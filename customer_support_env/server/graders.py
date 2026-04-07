"""Task graders for the Customer Support Resolution environment.

Each grader takes the episode state and ticket config, and returns
a score in [0.0, 1.0] based on deterministic keyword/structure matching.
"""

from typing import Any, Dict, List, Optional

from customer_support_env.models import SupportState


def _get_final_response(actions: List[Dict[str, Any]]) -> str:
    """Extract the final send_response or escalate content from actions."""
    for action in reversed(actions):
        if action["type"] in ("send_response", "escalate"):
            return action["content"]
    return ""


def _count_keyword_matches(text: str, keywords: List[str]) -> int:
    """Count how many keyword phrases appear in the text (case-insensitive)."""
    text_lower = text.lower()
    return sum(1 for kw in keywords if kw.lower() in text_lower)


def _searched_kb(actions: List[Dict[str, Any]]) -> bool:
    return any(a["type"] == "search_kb" for a in actions)


def grade_faq(state: SupportState, ticket_config: Dict[str, Any]) -> float:
    """Grade FAQ resolution task (Easy).

    Scoring:
      - Searched KB at all: 0.20
      - Found the correct KB article: 0.30
      - Solution keyword coverage: 0.50
    """
    score = 0.0
    actions = state.actions_taken

    # Searched KB
    if _searched_kb(actions):
        score += 0.20

    # Found correct article
    correct_ids = set(ticket_config["correct_kb_ids"])
    accessed_ids = set(state.kb_articles_accessed)
    if correct_ids & accessed_ids:
        score += 0.30

    # Solution keyword coverage
    response = _get_final_response(actions)
    if response:
        sol_kws = ticket_config["solution_keywords"]
        matched = _count_keyword_matches(response, sol_kws)
        ratio = matched / len(sol_kws) if sol_kws else 0
        score += 0.50 * ratio

    return min(score, 1.0)


def grade_troubleshooting(
    state: SupportState, ticket_config: Dict[str, Any]
) -> float:
    """Grade troubleshooting task (Medium).

    Scoring:
      - Searched KB: 0.15
      - Asked useful clarifying questions (max 2): 0.15
      - Found correct article: 0.20
      - Diagnosis keywords in response: 0.25
      - Solution keyword coverage: 0.25
    """
    score = 0.0
    actions = state.actions_taken

    # Searched KB
    if _searched_kb(actions):
        score += 0.15

    # Useful clarifications (count actions that got positive replies)
    qa_keys = set(ticket_config.get("clarification_qa", {}).keys())
    useful_count = 0
    for action in actions:
        if action["type"] == "ask_clarification":
            question_lower = action["content"].lower()
            for key in qa_keys:
                if key.lower() in question_lower:
                    useful_count += 1
                    break
    score += min(0.15, useful_count * 0.075)

    # Found correct article
    correct_ids = set(ticket_config["correct_kb_ids"])
    accessed_ids = set(state.kb_articles_accessed)
    if correct_ids & accessed_ids:
        score += 0.20

    # Diagnosis + solution in response
    response = _get_final_response(actions)
    if response:
        diag_kws = ticket_config.get("diagnosis_keywords", [])
        if diag_kws:
            diag_matched = _count_keyword_matches(response, diag_kws)
            score += 0.25 * (diag_matched / len(diag_kws))

        sol_kws = ticket_config["solution_keywords"]
        sol_matched = _count_keyword_matches(response, sol_kws)
        score += 0.25 * (sol_matched / len(sol_kws) if sol_kws else 0)

    return min(score, 1.0)


def grade_complex(state: SupportState, ticket_config: Dict[str, Any]) -> float:
    """Grade complex/escalation task (Hard).

    Scoring:
      - Sub-issues addressed in response: 0.30 (split equally)
      - Correct KB articles referenced: 0.20
      - Escalation decision correct: 0.20
      - Solution keyword coverage: 0.30
    """
    score = 0.0
    actions = state.actions_taken

    # Combine all action content for sub-issue detection
    all_content = " ".join(a["content"] for a in actions).lower()

    # Sub-issues addressed
    sub_issues = ticket_config.get("sub_issues", [])
    if sub_issues:
        per_sub = 0.30 / len(sub_issues)
        for sub in sub_issues:
            if any(kw.lower() in all_content for kw in sub["keywords"]):
                score += per_sub

    # Correct KB articles
    correct_ids = set(ticket_config["correct_kb_ids"])
    accessed_ids = set(state.kb_articles_accessed)
    found = correct_ids & accessed_ids
    if correct_ids:
        score += 0.20 * (len(found) / len(correct_ids))

    # Escalation decision
    should_escalate = ticket_config["should_escalate"]
    if should_escalate == state.escalated:
        score += 0.20

    # Solution keyword coverage
    response = _get_final_response(actions)
    if response:
        sol_kws = ticket_config["solution_keywords"]
        matched = _count_keyword_matches(response, sol_kws)
        score += 0.30 * (matched / len(sol_kws) if sol_kws else 0)

    return min(score, 1.0)


def grade_episode(
    state: SupportState, ticket_config: Dict[str, Any]
) -> float:
    """Grade an episode based on the task type. Returns score in [0, 1]."""
    task_id = state.task_id
    if task_id == "faq_resolution":
        return grade_faq(state, ticket_config)
    elif task_id == "troubleshooting":
        return grade_troubleshooting(state, ticket_config)
    elif task_id == "complex_escalation":
        return grade_complex(state, ticket_config)
    else:
        return 0.0
