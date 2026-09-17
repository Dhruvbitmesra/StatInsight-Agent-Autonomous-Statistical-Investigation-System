import pandas as pd

from tools.profiler import profile_dataset


df = pd.read_csv("data/sample.csv")

profile = profile_dataset(df)

print("Rows:", profile["rows"])
print("Columns:", profile["columns"])

print("\nNumerical columns:")
print(profile["numerical_columns"])

print("\nCategorical columns:")
print(profile["categorical_columns"])

print("\nMissing values:")
print(profile["missing_values"])

print("\nDuplicate rows:")
print(profile["duplicate_rows"])