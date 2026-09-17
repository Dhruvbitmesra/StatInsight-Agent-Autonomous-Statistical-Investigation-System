from agents.planner import create_investigation_plan
from tools.profiler import profile_dataset

import pandas as pd


df = pd.read_csv("data/sample.csv")

profile = profile_dataset(df)

question = "What factors are associated with passenger survival?"
plan = create_investigation_plan(
    question,
    profile
)

print("\nINVESTIGATION PLAN\n")
print(plan)