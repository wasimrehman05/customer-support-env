"""
Customer Support Resolution - Inference Script
================================================
Runs an LLM agent against the Customer Support environment for all 3 tasks.

MANDATORY ENV VARS:
    API_BASE_URL   The API endpoint for the LLM.
    MODEL_NAME     The model identifier to use for inference.
    HF_TOKEN       Your Hugging Face / API key.
    IMAGE_NAME     Docker image name (if using from_docker_image).

STDOUT FORMAT:
    [START] task=<task_name> env=<benchmark> model=<model_name>
    [STEP]  step=<n> action=<action_str> reward=<0.00> done=<true|false> error=<msg|null>
    [END]   success=<true|false> steps=<n> score=<score> rewards=<r1,r2,...,rn>
"""

import asyncio
import json
import os
import sys
import textwrap
from typing import Any, Dict, List, Optional

from openai import OpenAI

# Add parent dir to path so we can import the env package
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from customer_support_env import CustomerSupportEnv, SupportAction
from customer_support_env.server.graders import grade_episode
from customer_support_env.server.tickets import TICKETS

# ---- Configuration ----
IMAGE_NAME = os.getenv("IMAGE_NAME")
API_KEY = os.getenv("API_KEY") or os.getenv("HF_TOKEN")

API_BASE_URL = os.getenv("API_BASE_URL") or "https://router.huggingface.co/v1"
MODEL_NAME = os.getenv("MODEL_NAME") or "Qwen/Qwen2.5-72B-Instruct"
BENCHMARK = "customer_support_env"

MAX_TOKENS = 400
TEMPERATURE = 0.3

# Debug: log which credentials are being used
print(f"[DEBUG] API_BASE_URL={API_BASE_URL}", flush=True)
print(f"[DEBUG] MODEL_NAME={MODEL_NAME}", flush=True)
print(f"[DEBUG] API_KEY={'set (' + API_KEY[:8] + '...)' if API_KEY else 'NOT SET'}", flush=True)
print(f"[DEBUG] IMAGE_NAME={IMAGE_NAME}", flush=True)

# One representative ticket per task
TASKS = [
    {"task_id": "faq_resolution", "ticket_id": "T1-01", "max_steps": 8},
    {"task_id": "troubleshooting", "ticket_id": "T2-01", "max_steps": 12},
    {"task_id": "complex_escalation", "ticket_id": "T3-01", "max_steps": 15},
]

SYSTEM_PROMPT = textwrap.dedent("""\
You are a customer support agent for CloudDash, a cloud monitoring dashboard SaaS product.

You help resolve customer support tickets using these actions:
- search_kb: Search the knowledge base for relevant help articles
- ask_clarification: Ask the customer a specific clarifying question to better diagnose the issue
- send_response: Send your final resolution to the customer (ends the conversation)
- escalate: Escalate to senior team when the issue requires human intervention (e.g., billing disputes)

IMPORTANT: You must respond with ONLY a valid JSON object on a single line:
{"action_type": "<action>", "content": "<your text>"}

Required workflow:
1. ALWAYS start with search_kb on every new ticket. Never send a response without first searching the knowledge base — you do not know the product's exact procedures from memory.
2. Use specific, descriptive queries that capture the customer's issue.
3. If the ticket is missing key diagnostic details, ask focused clarifying questions about the specific aspects you need (one question at a time).
4. After gathering enough information, send_response with a thorough solution that includes the exact steps from the KB articles you found.
5. For complex tickets with multiple issues, address each sub-issue separately in the response.
6. Only escalate when the issue truly requires human review (billing disputes, security incidents).

The customer is depending on you. Ground your response in the KB articles, not in guesses.
""")


# ---- Logging helpers ----

def log_start(task: str, env: str, model: str) -> None:
    print(f"[START] task={task} env={env} model={model}", flush=True)


def log_step(
    step: int, action: str, reward: float, done: bool, error: Optional[str]
) -> None:
    error_val = error if error else "null"
    done_val = str(done).lower()
    # Truncate action to avoid overly long lines
    action_short = action.replace("\n", " ")[:200]
    print(
        f"[STEP] step={step} action={action_short} reward={reward:.2f} "
        f"done={done_val} error={error_val}",
        flush=True,
    )


def log_end(
    success: bool, steps: int, score: float, rewards: List[float]
) -> None:
    rewards_str = ",".join(f"{r:.2f}" for r in rewards)
    print(
        f"[END] success={str(success).lower()} steps={steps} "
        f"score={score:.2f} rewards={rewards_str}",
        flush=True,
    )


# ---- Agent logic ----

def build_user_prompt(obs_data: Dict[str, Any]) -> str:
    """Build the user prompt from the current observation."""
    parts = []

    ticket = obs_data.get("ticket", {})
    parts.append(f"CUSTOMER: {ticket.get('customer_name', 'Unknown')}")
    parts.append(f"ISSUE: {ticket.get('issue', '')}")
    parts.append(f"PRIORITY: {ticket.get('priority', 'medium')}")
    parts.append(f"CATEGORY: {ticket.get('category', 'General')}")
    parts.append(
        f"STEP: {obs_data.get('step_number', 0)}/{obs_data.get('max_steps', 15)}"
    )

    search_results = obs_data.get("search_results", [])
    if search_results:
        parts.append("\nSEARCH RESULTS:")
        for r in search_results:
            parts.append(f"  [{r['id']}] {r['title']} (relevance: {r.get('relevance_score', 0)})")
            snippet = r.get("content_snippet", "")
            if snippet:
                parts.append(f"    {snippet[:400]}")
            steps = r.get("solution_steps", [])
            if steps:
                parts.append(f"    Steps: {', '.join(steps)}")

    customer_reply = obs_data.get("customer_reply", "")
    if customer_reply:
        parts.append(f"\nCUSTOMER REPLY: {customer_reply}")

    system_msg = obs_data.get("system_message", "")
    if system_msg:
        parts.append(f"\nSYSTEM: {system_msg}")

    parts.append("\nRespond with your next action as JSON:")
    return "\n".join(parts)


def parse_action(text: str) -> SupportAction:
    """Parse LLM output into a SupportAction."""
    text = text.strip()

    # Try to extract JSON from the response
    # Handle cases where the LLM wraps JSON in markdown code blocks
    if "```" in text:
        for block in text.split("```"):
            block = block.strip()
            if block.startswith("json"):
                block = block[4:].strip()
            if block.startswith("{"):
                text = block
                break

    # Try direct JSON parse
    try:
        data = json.loads(text)
        if isinstance(data, dict) and "action_type" in data and "content" in data:
            action_type = data["action_type"]
            if action_type not in ("search_kb", "ask_clarification", "send_response", "escalate"):
                action_type = "send_response"
            return SupportAction(action_type=action_type, content=str(data["content"]))
    except json.JSONDecodeError:
        pass

    # Try to find JSON object in the text
    start = text.find("{")
    end = text.rfind("}") + 1
    if start >= 0 and end > start:
        try:
            data = json.loads(text[start:end])
            if "action_type" in data and "content" in data:
                return SupportAction(
                    action_type=data["action_type"], content=str(data["content"])
                )
        except json.JSONDecodeError:
            pass

    # Fallback: treat the entire response as send_response
    return SupportAction(action_type="send_response", content=text)


def get_agent_action(
    client: OpenAI,
    obs_data: Dict[str, Any],
    conversation_history: List[Dict[str, str]],
) -> SupportAction:
    """Call the LLM to decide the next action."""
    user_prompt = build_user_prompt(obs_data)
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    messages.extend(conversation_history)
    messages.append({"role": "user", "content": user_prompt})

    try:
        completion = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            temperature=TEMPERATURE,
            max_tokens=MAX_TOKENS,
            stream=False,
        )
        response_text = (completion.choices[0].message.content or "").strip()
        if not response_text:
            return SupportAction(action_type="send_response", content="I apologize, I need more information.")

        action = parse_action(response_text)

        # Add to conversation history
        conversation_history.append({"role": "user", "content": user_prompt})
        conversation_history.append({"role": "assistant", "content": response_text})

        return action
    except Exception as exc:
        print(f"[DEBUG] Model request failed: {exc}", flush=True)
        return SupportAction(
            action_type="send_response",
            content="I apologize for the difficulty. Let me connect you with a specialist.",
        )


# ---- Main loop ----

async def run_task(
    client: OpenAI,
    task_id: str,
    ticket_id: str,
    max_steps: int,
) -> float:
    """Run a single task episode and return the score."""
    env = None
    rewards: List[float] = []
    steps_taken = 0
    score = 0.0
    success = False

    log_start(task=task_id, env=BENCHMARK, model=MODEL_NAME)

    try:
        # Connect to environment
        if IMAGE_NAME:
            env = await CustomerSupportEnv.from_docker_image(IMAGE_NAME)
        else:
            # Run environment in-process for simplicity
            from customer_support_env.server.environment import CustomerSupportEnvironment
            from customer_support_env.server.graders import grade_episode as _grade

            local_env = CustomerSupportEnvironment()
            obs = local_env.reset(task_id=task_id, ticket_id=ticket_id)

            obs_data = {
                "ticket": obs.ticket,
                "search_results": obs.search_results,
                "customer_reply": obs.customer_reply,
                "system_message": obs.system_message,
                "available_actions": obs.available_actions,
                "step_number": obs.step_number,
                "max_steps": obs.max_steps,
            }

            conversation_history: List[Dict[str, str]] = []

            for step_num in range(1, max_steps + 1):
                if obs.done:
                    break

                action = get_agent_action(client, obs_data, conversation_history)

                obs = local_env.step(action)
                reward = obs.reward or 0.0
                done = obs.done
                error = None

                rewards.append(reward)
                steps_taken = step_num

                action_str = f"{action.action_type}:{action.content[:100]}"
                log_step(
                    step=step_num,
                    action=action_str,
                    reward=reward,
                    done=done,
                    error=error,
                )

                obs_data = {
                    "ticket": obs.ticket,
                    "search_results": obs.search_results,
                    "customer_reply": obs.customer_reply,
                    "system_message": obs.system_message,
                    "available_actions": obs.available_actions,
                    "step_number": obs.step_number,
                    "max_steps": obs.max_steps,
                }

                if done:
                    break

            # Compute final score using grader
            ticket_config = TICKETS[ticket_id]
            score = _grade(local_env.state, ticket_config)
            score = min(max(score, 0.0), 1.0)
            success = score >= 0.1

    except Exception as e:
        print(f"[DEBUG] Task {task_id} error: {e}", flush=True)
    finally:
        if env:
            try:
                await env.close()
            except Exception:
                pass
        log_end(success=success, steps=steps_taken, score=score, rewards=rewards)

    return score


async def main() -> None:
    client = OpenAI(base_url=API_BASE_URL, api_key=API_KEY)

    total_score = 0.0
    for task_cfg in TASKS:
        score = await run_task(
            client=client,
            task_id=task_cfg["task_id"],
            ticket_id=task_cfg["ticket_id"],
            max_steps=task_cfg["max_steps"],
        )
        total_score += score

    avg_score = total_score / len(TASKS)
    print(f"[DEBUG] Average score across {len(TASKS)} tasks: {avg_score:.3f}", flush=True)


if __name__ == "__main__":
    asyncio.run(main())
