from typing import Any, Dict

from openenv.core.env_client import EnvClient
from openenv.core.client_types import StepResult

from customer_support_env.models import (
    SupportAction,
    SupportObservation,
    SupportState,
)


class CustomerSupportEnv(EnvClient[SupportAction, SupportObservation, SupportState]):
    """Client for the Customer Support Resolution environment."""

    def _step_payload(self, action: SupportAction) -> dict:
        return {
            "action_type": action.action_type,
            "content": action.content,
        }

    def _parse_result(self, payload: dict) -> StepResult:
        obs_data = payload.get("observation", payload)
        obs = SupportObservation(
            done=payload.get("done", obs_data.get("done", False)),
            reward=payload.get("reward", obs_data.get("reward")),
            ticket=obs_data.get("ticket", {}),
            search_results=obs_data.get("search_results", []),
            customer_reply=obs_data.get("customer_reply", ""),
            system_message=obs_data.get("system_message", ""),
            available_actions=obs_data.get("available_actions", []),
            step_number=obs_data.get("step_number", 0),
            max_steps=obs_data.get("max_steps", 15),
            metadata=obs_data.get("metadata", {}),
        )
        return StepResult(
            observation=obs,
            reward=payload.get("reward", obs_data.get("reward")),
            done=payload.get("done", obs_data.get("done", False)),
        )

    def _parse_state(self, payload: dict) -> SupportState:
        return SupportState(**payload)
