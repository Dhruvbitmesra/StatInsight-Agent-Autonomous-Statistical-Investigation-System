from typing import TypedDict, Any


class AgentState(TypedDict, total=False):

    question: str
    dataset_path: str

    dataset_profile: dict[str, Any]

    investigation_plan: list[str]
    current_task: str
    completed_tasks: list[str]
    investigation_decision: dict

    analysis_results: list[dict[str, Any]]
    generated_code: str
    execution_error: str

    critic_feedback: str
    evidence_sufficient: bool

    final_report: str

    iteration: int