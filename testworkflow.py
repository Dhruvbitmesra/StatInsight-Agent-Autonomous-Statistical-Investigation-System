from graph.workflow import workflow


initial_state = {
    "question": "Determine whether Sex is associated with passenger survival.",
    "dataset_path": "data/sample.csv",
}


result = workflow.invoke(initial_state)


print("\n==============================")
print("INVESTIGATION PLAN")
print("==============================")

for task in result["investigation_plan"]:
    print("-", task)


print("\n==============================")
print("CURRENT TASK")
print("==============================")

print(result["current_task"])


print("\n==============================")
print("INVESTIGATOR DECISION")
print("==============================")

print(result["investigation_decision"])


print("\n==============================")
print("ANALYSIS RESULT")
print("==============================")

print(result["analysis_results"])