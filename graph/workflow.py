import pandas as pd

from langgraph.graph import StateGraph, START, END

from graph.state import AgentState
from tools.profiler import profile_dataset
from agents.planner import create_investigation_plan
from agents.investigator import select_analysis_tool
from tools.executor import execute_analysis


# --------------------------------------------------
# NODE 1 — PROFILE DATASET
# --------------------------------------------------

def profile_node(state: AgentState):

    df = pd.read_csv(state["dataset_path"])

    profile = profile_dataset(df)

    return {
        "dataset_profile": profile
    }


# --------------------------------------------------
# NODE 2 — CREATE INVESTIGATION PLAN
# --------------------------------------------------

def planner_node(state: AgentState):

    plan = create_investigation_plan(
        state["question"],
        state["dataset_profile"],
    )

    # Convert numbered text into a list of tasks
    tasks = []

    for line in plan.splitlines():

        line = line.strip()

        if not line:
            continue

        # Remove common numbering formats:
        # 1. Task
        # 2) Task
        # - Task

        cleaned = line.lstrip("0123456789.-) ").strip()

        if cleaned:
            tasks.append(cleaned)

    return {
        "investigation_plan": tasks,
        "completed_tasks": [],
        "analysis_results": [],
    }


# --------------------------------------------------
# NODE 3 — INVESTIGATE FIRST TASK
# --------------------------------------------------

def investigator_node(state: AgentState):

    task = state["investigation_plan"][0]

    decision = select_analysis_tool(
        state["dataset_profile"],
        task,
    )

    return {
        "current_task": task,
        "investigation_decision": decision.model_dump(),
    }


# --------------------------------------------------
# NODE 4 — EXECUTE ANALYSIS
# --------------------------------------------------

def execute_node(state: AgentState):

    df = pd.read_csv(
        state["dataset_path"]
    )

    # Reconstruct the decision object
    from agents.investigator import AnalysisDecision

    decision = AnalysisDecision(
        **state["investigation_decision"]
    )

    result = execute_analysis(
        df,
        decision,
    )

    results = state.get(
        "analysis_results",
        []
    )

    results.append(
        {
            "task": state["current_task"],
            "analysis": result,
        }
    )

    completed = state.get(
        "completed_tasks",
        []
    )

    completed.append(
        state["current_task"]
    )

    return {
        "analysis_results": results,
        "completed_tasks": completed,
    }


# --------------------------------------------------
# BUILD GRAPH
# --------------------------------------------------

builder = StateGraph(AgentState)

builder.add_node(
    "profile",
    profile_node,
)

builder.add_node(
    "planner",
    planner_node,
)

builder.add_node(
    "investigator",
    investigator_node,
)

builder.add_node(
    "execute",
    execute_node,
)


# --------------------------------------------------
# EDGES
# --------------------------------------------------

builder.add_edge(
    START,
    "profile",
)

builder.add_edge(
    "profile",
    "planner",
)

builder.add_edge(
    "planner",
    "investigator",
)

builder.add_edge(
    "investigator",
    "execute",
)

builder.add_edge(
    "execute",
    END,
)


# --------------------------------------------------
# COMPILE GRAPH
# --------------------------------------------------

workflow = builder.compile()