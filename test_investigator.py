import pandas as pd

from tools.profiler import profile_dataset
from agents.investigator import select_analysis_tool


df = pd.read_csv("data/sample.csv")

profile = profile_dataset(df)


task = "Determine whether Sex is associated with passenger survival."


result = select_analysis_tool(
    profile,
    task,
)


print("\nINVESTIGATOR DECISION\n")
print(result)