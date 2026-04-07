---
title: Customer Support Resolution Environment
emoji: 🎧
colorFrom: blue
colorTo: purple
sdk: docker
app_port: 8000
tags:
  - openenv
---

# Customer Support Resolution Environment

An OpenEnv environment where an AI agent resolves customer support tickets for **CloudDash**, a fictional cloud monitoring SaaS product. The agent must search a knowledge base, ask clarifying questions, and provide accurate solutions -- just like a real support agent.

## Why This Environment?

Customer support is a **universal business problem** that every company faces. Training AI agents to handle support tickets effectively could save billions in operational costs while improving customer satisfaction. This environment provides a realistic, multi-step simulation of the support resolution workflow with deterministic, reproducible grading.

## Action Space

The agent sends actions as `{"action_type": str, "content": str}`:

| Action | Description | When to Use |
|--------|-------------|-------------|
| `search_kb` | Search the knowledge base | To find relevant help articles |
| `ask_clarification` | Ask customer a question | When the issue needs more details |
| `send_response` | Send resolution to customer | When ready to resolve (ends episode) |
| `escalate` | Escalate to senior team | For billing disputes / security issues (ends episode) |

## Observation Space

After each action, the agent receives:

| Field | Type | Description |
|-------|------|-------------|
| `ticket` | dict | Customer name, issue description, priority, category |
| `search_results` | list[dict] | KB articles: id, title, category, relevance, snippet, steps |
| `customer_reply` | str | Customer's answer to clarifying questions |
| `system_message` | str | Environment feedback on the action taken |
| `available_actions` | list[str] | Valid actions in current state |
| `step_number` | int | Current step number |
| `max_steps` | int | Maximum steps allowed for this task |
| `done` | bool | Whether the episode has ended |
| `reward` | float | Reward for the last action |

## Tasks

### Task 1: FAQ Resolution (Easy)
- **Max steps:** 8
- **Objective:** Answer simple questions with direct knowledge base matches
- **Example:** "How do I reset my password?"
- **Strategy:** Search KB -> find article -> send solution with key steps

### Task 2: Troubleshooting (Medium)
- **Max steps:** 12
- **Objective:** Diagnose technical issues that require investigation
- **Example:** "My dashboard isn't loading" (could be cache, extension, or data source issue)
- **Strategy:** Ask clarifying questions -> narrow down cause -> search KB -> send diagnosis + fix

### Task 3: Complex / Escalation (Hard)
- **Max steps:** 15
- **Objective:** Handle multi-issue tickets where some parts need escalation
- **Example:** "Double-charged on upgrade AND team can't access dashboard AND API errors"
- **Strategy:** Decompose issues -> solve what's possible -> escalate billing disputes -> address all sub-issues

## Reward Design

Partial rewards per step (not binary end-of-episode):
- Found correct KB article: **+0.15**
- Useful clarifying question: **+0.10**
- Correct diagnosis in response: **+0.20**
- Solution keyword coverage: **+0.25**
- Sub-issue addressed (complex): **+0.10** each
- Correct escalation decision: **+0.15**
- Irrelevant/redundant actions: **-0.03 to -0.10**

Final score normalized to [0.0, 1.0].

## Knowledge Base

15 articles covering:
- **Account** (3): Password reset, 2FA setup, team permissions
- **Billing** (3): Billing statements, plan changes, refunds
- **Technical** (5): Dashboard loading, data sources, alerts, API, data sync
- **Features** (2): Custom widgets, report export
- **Policies** (2): SLA/uptime, escalation policy

## Setup

### Local Development
```bash
pip install openenv-core[core] fastapi pydantic uvicorn openai
PYTHONPATH=. uvicorn customer_support_env.server.app:app --host 0.0.0.0 --port 8000
```

### Docker
```bash
docker build -t customer-support-env .
docker run -p 8000:8000 customer-support-env
```

### Run Inference
```bash
export API_BASE_URL="https://router.huggingface.co/v1"
export MODEL_NAME="Qwen/Qwen2.5-72B-Instruct"
export HF_TOKEN="your-token-here"
python inference.py
```

## API Endpoints

- `POST /reset` — Start a new ticket episode
- `POST /step` — Take an action
- `GET /state` — Get current environment state
- `GET /health` — Health check
- `WebSocket /ws` — Persistent session connection

## Baseline Scores

| Task | Score | Steps |
|------|-------|-------|
| FAQ Resolution (Easy) | ~0.85-1.00 | 2-3 |
| Troubleshooting (Medium) | ~0.60-0.80 | 4-6 |
| Complex/Escalation (Hard) | ~0.40-0.60 | 6-10 |

## Project Structure

```
├── inference.py                     # Inference script (root)
├── Dockerfile                       # Container definition
├── README.md                        # This file
└── customer_support_env/
    ├── __init__.py                  # Package exports
    ├── models.py                    # Pydantic: Action, Observation, State
    ├── client.py                    # EnvClient subclass
    ├── openenv.yaml                 # OpenEnv manifest
    ├── pyproject.toml               # Dependencies
    └── server/
        ├── __init__.py
        ├── app.py                   # FastAPI app (create_fastapi_app)
        ├── environment.py           # Core environment logic
        ├── knowledge_base.py        # 15 KB articles + search
        ├── tickets.py               # 11 ticket scenarios
        ├── graders.py               # Task grading functions
        ├── requirements.txt         # Python dependencies
        └── Dockerfile               # Server Dockerfile
```
