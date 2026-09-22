import pandas as pd

from langgraph.graph import StateGraph, START, END

from graph.state import AgentState

from tools.profiler import profile_dataset

from agents.planner import (
    create_investigation_plan
)

from agents.investigator import (
    select_analysis_tool,
    AnalysisDecision,
)

from tools.executor import (
    execute_analysis
)

from agents.critic import (
    evaluate_evidence
)

from agents.reporter import (
    generate_final_report
)


# ==================================================
# NODE 1 — PROFILE DATASET
# ==================================================

def profile_node(state: AgentState):

    print("\n")
    print("=" * 70)
    print("PROFILING DATASET")
    print("=" * 70)

    df = pd.read_csv(
        state["dataset_path"]
    )

    profile = profile_dataset(df)

    print(
        f"Rows: {profile['rows']}"
    )

    print(
        f"Columns: {profile['columns']}"
    )

    return {
        "dataset_profile": profile
    }


# ==================================================
# NODE 2 — CREATE INVESTIGATION PLAN
# ==================================================

def planner_node(state: AgentState):

    print("\n")
    print("=" * 70)
    print("CREATING INVESTIGATION PLAN")
    print("=" * 70)

    plan = create_investigation_plan(
        state["question"],
        state["dataset_profile"],
    )

    tasks = []

    for line in plan.splitlines():

        line = line.strip()

        if not line:
            continue

        cleaned = line.lstrip(
            "0123456789.-) "
        ).strip()

        if cleaned:
            tasks.append(cleaned)

    # Remove accidental empty tasks
    tasks = [
        task
        for task in tasks
        if task.strip()
    ]

    if not tasks:

        raise ValueError(
            "Planner generated an empty investigation plan."
        )

    print("\nGenerated Investigation Plan:")

    for i, task in enumerate(
        tasks,
        start=1
    ):
        print(
            f"{i}. {task}"
        )

    return {

        "investigation_plan": tasks,

        "current_task_index": 0,

        "completed_tasks": [],

        "analysis_results": [],

        "iteration": 0,
    }


# ==================================================
# NODE 3 — GET CURRENT TASK
# ==================================================

def task_node(state: AgentState):

    plan = state.get(
        "investigation_plan",
        []
    )

    completed_tasks = state.get(
        "completed_tasks",
        []
    )

    current_index = len(
        completed_tasks
    )

    # Safety check
    if current_index >= len(plan):

        return {}

    current_task = plan[
        current_index
    ]

    print("\n")
    print("=" * 70)

    print(
        f"CURRENT TASK "
        f"{current_index + 1}/{len(plan)}"
    )

    print("=" * 70)

    print(
        current_task
    )

    return {

        "current_task":
            current_task,

        "current_task_index":
            current_index,
    }


# ==================================================
# NODE 4 — INVESTIGATOR
# ==================================================

def investigator_node(state: AgentState):

    current_task = state.get(
        "current_task"
    )

    if not current_task:

        raise ValueError(
            "No current investigation task found."
        )

    decision = select_analysis_tool(

        state["dataset_profile"],

        current_task,
    )

    print("\nSelected Analysis Tool:")

    print(
        decision.tool
    )

    print("\nReason:")

    print(
        decision.reason
    )

    return {

        "investigation_decision":
            decision.model_dump()
    }


# ==================================================
# NODE 5 — EXECUTE ANALYSIS
# ==================================================

def execute_node(state: AgentState):

    df = pd.read_csv(
        state["dataset_path"]
    )

    decision_data = state.get(
        "investigation_decision"
    )

    if not decision_data:

        raise ValueError(
            "Investigator did not produce "
            "an analysis decision."
        )

    decision = AnalysisDecision(
        **decision_data
    )

    print("\nExecuting:")

    print(
        decision.tool
    )

    result = execute_analysis(

        df,

        decision,
    )

    # ----------------------------------------------
    # Previous analysis results
    # ----------------------------------------------

    results = list(
        state.get(
            "analysis_results",
            []
        )
    )

    results.append(
        {
            "task":
                state["current_task"],

            "tool":
                decision.tool,

            "analysis":
                result,
        }
    )

    # ----------------------------------------------
    # Previous completed tasks
    # ----------------------------------------------

    completed = list(
        state.get(
            "completed_tasks",
            []
        )
    )

    completed.append(
        state["current_task"]
    )

    # ----------------------------------------------
    # Current index
    # ----------------------------------------------

    current_index = len(
        completed
    )

    return {

        "analysis_results":
            results,

        "completed_tasks":
            completed,

        "current_task_index":
            current_index,

        "iteration":
            state.get(
                "iteration",
                0
            ) + 1,
    }


# ==================================================
# NODE 6 — CRITIC
# ==================================================

def critic_node(state: AgentState):

    print("\n")
    print("=" * 70)
    print("CRITIC")
    print("=" * 70)

    decision = evaluate_evidence(

        question=
            state["question"],

        investigation_plan=
            state.get(
                "investigation_plan",
                []
            ),

        completed_tasks=
            state.get(
                "completed_tasks",
                []
            ),

        analysis_results=
            state.get(
                "analysis_results",
                []
            ),
    )

    print(
        "\nEvidence sufficient:",
        decision.evidence_sufficient
    )

    print(
        "\nCritic feedback:"
    )

    print(
        decision.feedback
    )

    return {

        "evidence_sufficient":
            decision.evidence_sufficient,

        "critic_feedback":
            decision.feedback,
    }


# ==================================================
# NODE 7 — FINAL REPORT
# ==================================================

def report_node(state: AgentState):

    print("\n")
    print("=" * 70)
    print("GENERATING FINAL REPORT")
    print("=" * 70)

    report = generate_final_report(

        question=
            state["question"],

        investigation_plan=
            state.get(
                "investigation_plan",
                []
            ),

        completed_tasks=
            state.get(
                "completed_tasks",
                []
            ),

        analysis_results=
            state.get(
                "analysis_results",
                []
            ),

        critic_feedback=
            state.get(
                "critic_feedback",
                ""
            ),
    )

    return {

        "final_report":
            report
    }


# ==================================================
# ROUTER
# ==================================================

def route_next_task(state: AgentState):

    plan = state.get(
        "investigation_plan",
        []
    )

    completed_tasks = state.get(
        "completed_tasks",
        []
    )

    completed_count = len(
        completed_tasks
    )

    total_tasks = len(
        plan
    )

    print("\nRouter:")

    print(
        f"Completed: "
        f"{completed_count}/{total_tasks}"
    )

    # ----------------------------------------------
    # More tasks remain
    # ----------------------------------------------

    if completed_count < total_tasks:

        return "task"

    # ----------------------------------------------
    # All tasks completed
    # ----------------------------------------------

    return "critic"


# ==================================================
# BUILD GRAPH
# ==================================================

builder = StateGraph(
    AgentState
)


# ==================================================
# ADD NODES
# ==================================================

builder.add_node(
    "profile",
    profile_node
)

builder.add_node(
    "planner",
    planner_node
)

builder.add_node(
    "task",
    task_node
)

builder.add_node(
    "investigator",
    investigator_node
)

builder.add_node(
    "execute",
    execute_node
)

builder.add_node(
    "critic",
    critic_node
)

builder.add_node(
    "report",
    report_node
)


# ==================================================
# GRAPH EDGES
# ==================================================

builder.add_edge(
    START,
    "profile"
)

builder.add_edge(
    "profile",
    "planner"
)

builder.add_edge(
    "planner",
    "task"
)

builder.add_edge(
    "task",
    "investigator"
)

builder.add_edge(
    "investigator",
    "execute"
)


# ==================================================
# CONDITIONAL ROUTING
# ==================================================

builder.add_conditional_edges(

    "execute",

    route_next_task,

    {
        "task":
            "task",

        "critic":
            "critic",
    }
)


# ==================================================
# FINAL FLOW
# ==================================================

builder.add_edge(
    "critic",
    "report"
)

builder.add_edge(
    "report",
    END
)


# ==================================================
# COMPILE
# ==================================================

workflow = builder.compile()