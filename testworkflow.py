from graph.workflow import workflow


# ==================================================
# INITIAL INPUT
# ==================================================

initial_state = {
    "question": (
        "What factors are associated "
        "with passenger survival?"
    ),

    "dataset_path": "data/sample.csv",
}


# ==================================================
# RUN COMPLETE WORKFLOW
# ==================================================

print("\n")
print("=" * 70)
print("STARTING STATAGENT")
print("=" * 70)

result = workflow.invoke(
    initial_state
)


# ==================================================
# 1. INVESTIGATION PLAN
# ==================================================

print("\n")
print("=" * 70)
print("1. INVESTIGATION PLAN")
print("=" * 70)

for i, task in enumerate(
    result["investigation_plan"],
    start=1,
):
    print(f"{i}. {task}")


# ==================================================
# 2. COMPLETED TASKS
# ==================================================

print("\n")
print("=" * 70)
print("2. COMPLETED TASKS")
print("=" * 70)

for i, task in enumerate(
    result["completed_tasks"],
    start=1,
):
    print(f"{i}. {task}")


# ==================================================
# 3. ANALYSIS RESULTS
# ==================================================

print("\n")
print("=" * 70)
print("3. ANALYSIS RESULTS")
print("=" * 70)

for i, item in enumerate(
    result["analysis_results"],
    start=1,
):

    print(f"\nAnalysis {i}")
    print("-" * 50)

    print("Task:")
    print(item["task"])

    print("\nResult:")
    print(item["analysis"])


# ==================================================
# 4. CRITIC
# ==================================================

print("\n")
print("=" * 70)
print("4. CRITIC")
print("=" * 70)

print(
    "Evidence sufficient:",
    result["evidence_sufficient"],
)

print("\nCritic feedback:")
print(result["critic_feedback"])


# ==================================================
# 5. FINAL REPORT
# ==================================================

print("\n")
print("=" * 70)
print("5. FINAL REPORT")
print("=" * 70)

print(result["final_report"])


# ==================================================
# FINAL STATUS
# ==================================================

print("\n")
print("=" * 70)
print("STATAGENT PIPELINE COMPLETED")
print("=" * 70)