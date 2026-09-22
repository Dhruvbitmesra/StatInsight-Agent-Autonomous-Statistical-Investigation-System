from typing import TypedDict, Any


class AgentState(TypedDict, total=False):

    # ==================================================
    # USER INPUT
    # ==================================================

    question: str
    dataset_path: str


    # ==================================================
    # DATASET
    # ==================================================

    dataset_profile: dict[str, Any]


    # ==================================================
    # INVESTIGATION
    # ==================================================

    investigation_plan: list[str]

    current_task: str

    current_task_index: int

    completed_tasks: list[str]

    investigation_decision: dict[str, Any]


    # ==================================================
    # ANALYSIS
    # ==================================================

    analysis_results: list[dict[str, Any]]

    generated_code: str

    execution_error: str


    # ==================================================
    # VALIDATION
    # ==================================================

    critic_feedback: str

    evidence_sufficient: bool


    # ==================================================
    # FINAL OUTPUT
    # ==================================================

    final_report: str


    # ==================================================
    # CONTROL
    # ==================================================

    iteration: int