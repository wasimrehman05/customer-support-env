from typing import List, Dict, Any, Optional
from pydantic import Field

from openenv.core.env_server import Action, Observation, State


class SupportAction(Action):
    """Action the agent can take in the customer support environment."""

    action_type: str = Field(
        description="One of: search_kb, ask_clarification, send_response, escalate"
    )
    content: str = Field(
        description="The query, question, response text, or escalation reason"
    )


class SupportObservation(Observation):
    """What the agent observes after each step."""

    ticket: Dict[str, Any] = Field(
        default_factory=dict,
        description="Current ticket info: customer_name, issue, priority, category",
    )
    search_results: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="KB articles returned from search_kb action",
    )
    customer_reply: str = Field(
        default="",
        description="Simulated customer reply to clarifying questions",
    )
    system_message: str = Field(
        default="",
        description="Feedback from the environment",
    )
    available_actions: List[str] = Field(
        default_factory=list,
        description="Valid action types in current state",
    )
    step_number: int = Field(default=0, description="Current step number")
    max_steps: int = Field(default=15, description="Maximum steps for this episode")


class SupportState(State):
    """Internal environment state for the current episode."""

    task_id: str = ""
    ticket_id: str = ""
    actions_taken: List[Dict[str, Any]] = Field(default_factory=list)
    kb_articles_accessed: List[str] = Field(default_factory=list)
    clarifications_asked: int = 0
    resolved: bool = False
    escalated: bool = False
