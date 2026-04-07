import random
import uuid
from typing import Any, Dict, List, Optional

from openenv.core.env_server import Environment

from customer_support_env.models import (
    SupportAction,
    SupportObservation,
    SupportState,
)
from customer_support_env.server.knowledge_base import search_knowledge_base
from customer_support_env.server.tickets import TASK_TICKETS, TICKETS


VALID_ACTIONS = {"search_kb", "ask_clarification", "send_response", "escalate"}


class CustomerSupportEnvironment(Environment[SupportAction, SupportObservation, SupportState]):
    """OpenEnv environment for customer support ticket resolution.

    The agent receives a support ticket and must resolve it by searching
    a knowledge base, asking clarifying questions, and sending a response
    (or escalating when appropriate).
    """

    SUPPORTS_CONCURRENT_SESSIONS = True

    def __init__(self) -> None:
        super().__init__()
        self._state = SupportState()
        self._ticket_config: Dict[str, Any] = {}
        self._cumulative_reward: float = 0.0
        self._searched_queries: set = set()
        self._matched_clarifications: set = set()

    def reset(
        self,
        seed: Optional[int] = None,
        episode_id: Optional[str] = None,
        **kwargs: Any,
    ) -> SupportObservation:
        """Start a new support ticket episode."""
        task_id = kwargs.get("task_id", "faq_resolution")
        ticket_id = kwargs.get("ticket_id", None)

        if seed is not None:
            random.seed(seed)

        if ticket_id is None:
            available = TASK_TICKETS.get(task_id, TASK_TICKETS["faq_resolution"])
            ticket_id = random.choice(available)

        self._ticket_config = TICKETS[ticket_id]
        self._cumulative_reward = 0.0
        self._searched_queries = set()
        self._matched_clarifications = set()

        self._state = SupportState(
            episode_id=episode_id or str(uuid.uuid4()),
            step_count=0,
            task_id=task_id,
            ticket_id=ticket_id,
            actions_taken=[],
            kb_articles_accessed=[],
            clarifications_asked=0,
            resolved=False,
            escalated=False,
        )

        return SupportObservation(
            done=False,
            reward=None,
            ticket=self._build_ticket_info(),
            search_results=[],
            customer_reply="",
            system_message=(
                f"New support ticket from {self._ticket_config['customer_name']}. "
                f"Priority: {self._ticket_config['priority']}. "
                f"Category: {self._ticket_config['category']}. "
                f"Please help resolve this issue."
            ),
            available_actions=list(VALID_ACTIONS),
            step_number=0,
            max_steps=self._ticket_config["max_steps"],
            metadata={"task_id": task_id, "ticket_id": ticket_id},
        )

    def step(
        self,
        action: SupportAction,
        timeout_s: Optional[float] = None,
        **kwargs: Any,
    ) -> SupportObservation:
        """Process an agent action and return the next observation."""
        self._state.step_count += 1
        step_reward = 0.0
        search_results: List[Dict[str, Any]] = []
        customer_reply = ""
        system_message = ""
        done = False

        # Record action
        self._state.actions_taken.append(
            {
                "type": action.action_type,
                "content": action.content,
                "step": self._state.step_count,
            }
        )

        if action.action_type not in VALID_ACTIONS:
            system_message = (
                f"Unknown action type: '{action.action_type}'. "
                f"Valid actions: {', '.join(sorted(VALID_ACTIONS))}"
            )
            step_reward = -0.05
        elif action.action_type == "search_kb":
            step_reward, search_results, system_message = self._handle_search(
                action.content
            )
        elif action.action_type == "ask_clarification":
            step_reward, customer_reply, system_message = (
                self._handle_clarification(action.content)
            )
        elif action.action_type == "send_response":
            step_reward, system_message = self._handle_response(action.content)
            self._state.resolved = True
            done = True
        elif action.action_type == "escalate":
            step_reward, system_message = self._handle_escalate(action.content)
            self._state.escalated = True
            done = True

        # Check max steps
        if self._state.step_count >= self._ticket_config["max_steps"] and not done:
            done = True
            system_message += " [Episode ended: maximum steps reached]"

        self._cumulative_reward += step_reward

        return SupportObservation(
            done=done,
            reward=step_reward,
            ticket=self._build_ticket_info(),
            search_results=search_results,
            customer_reply=customer_reply,
            system_message=system_message,
            available_actions=[] if done else list(VALID_ACTIONS),
            step_number=self._state.step_count,
            max_steps=self._ticket_config["max_steps"],
            metadata={
                "task_id": self._state.task_id,
                "ticket_id": self._state.ticket_id,
                "cumulative_reward": round(self._cumulative_reward, 4),
            },
        )

    @property
    def state(self) -> SupportState:
        """Return current environment state."""
        return self._state

    def close(self) -> None:
        """Clean up resources."""
        pass

    # ----- internal handlers -----

    def _build_ticket_info(self) -> Dict[str, Any]:
        return {
            "customer_name": self._ticket_config["customer_name"],
            "issue": self._ticket_config["issue"],
            "priority": self._ticket_config["priority"],
            "category": self._ticket_config["category"],
        }

    def _handle_search(self, query: str):
        query_key = query.lower().strip()
        if query_key in self._searched_queries:
            return (
                -0.03,
                [],
                "You already searched for this query. Try different search terms.",
            )
        self._searched_queries.add(query_key)

        results = search_knowledge_base(query, top_k=3)
        found_ids = [r["id"] for r in results]
        self._state.kb_articles_accessed.extend(found_ids)

        correct_ids = set(self._ticket_config["correct_kb_ids"])

        if any(rid in correct_ids for rid in found_ids):
            reward = 0.15
            msg = (
                f"Search returned {len(results)} result(s). "
                f"Relevant articles found for this issue."
            )
        elif results:
            reward = 0.05
            msg = f"Search returned {len(results)} result(s), but none are a direct match."
        else:
            reward = -0.05
            msg = "No results found. Try different or more specific search terms."

        return reward, results, msg

    def _handle_clarification(self, question: str):
        self._state.clarifications_asked += 1
        qa_map = self._ticket_config.get("clarification_qa", {})

        question_lower = question.lower()
        matched_answer = None
        matched_key = None

        for key, answer in qa_map.items():
            if key.lower() in question_lower and key not in self._matched_clarifications:
                matched_answer = answer
                matched_key = key
                break

        if matched_answer and matched_key:
            self._matched_clarifications.add(matched_key)
            return (
                0.075,
                matched_answer,
                "Customer replied to your question.",
            )
        elif matched_key is None and any(
            k.lower() in question_lower for k in qa_map
        ):
            return (
                -0.03,
                "You already asked about this. Is there anything else you need to know?",
                "Customer already answered a similar question.",
            )
        else:
            return (
                -0.05,
                (
                    "I'm not sure what you're asking. Could you be more specific "
                    "about what information you need?"
                ),
                "Customer didn't understand the question. Try asking about specific details.",
            )

    def _handle_response(self, response: str):
        response_lower = response.lower()

        # Score solution keywords
        solution_kws = self._ticket_config["solution_keywords"]
        matched_sol = sum(1 for kw in solution_kws if kw.lower() in response_lower)
        sol_ratio = matched_sol / len(solution_kws) if solution_kws else 0

        reward = 0.25 * sol_ratio

        # Score diagnosis keywords (troubleshooting / complex tasks)
        diag_kws = self._ticket_config.get("diagnosis_keywords", [])
        if diag_kws:
            matched_diag = sum(1 for kw in diag_kws if kw.lower() in response_lower)
            diag_ratio = matched_diag / len(diag_kws)
            reward += 0.20 * diag_ratio

        # Score sub-issue coverage (complex tasks)
        sub_issues = self._ticket_config.get("sub_issues", [])
        for sub in sub_issues:
            if any(kw.lower() in response_lower for kw in sub["keywords"]):
                reward += 0.10

        pct = sol_ratio * 100
        msg = f"Response sent to customer. Solution coverage: {pct:.0f}%."
        if sol_ratio >= 0.8:
            msg += " Excellent response!"
        elif sol_ratio >= 0.5:
            msg += " Good, but some details could be improved."
        else:
            msg += " The response is missing key solution steps."

        return reward, msg

    def _handle_escalate(self, reason: str):
        should_escalate = self._ticket_config["should_escalate"]
        if should_escalate:
            return (
                0.15,
                (
                    "Ticket correctly escalated to the senior support team. "
                    "A specialist will handle the billing/security aspects."
                ),
            )
        else:
            return (
                -0.10,
                (
                    "This ticket could have been resolved without escalation. "
                    "Unnecessary escalation wastes senior team resources."
                ),
            )
