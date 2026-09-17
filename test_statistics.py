import pandas as pd

from tools.statistics import (
    descriptive_statistics,
    group_analysis,
    correlation_analysis,
    hypothesis_test,
)


df = pd.read_csv("data/sample.csv")


print("\n--- DESCRIPTIVE STATISTICS ---")

print(
    descriptive_statistics(
        df,
        "Age",
    )
)


print("\n--- GROUP ANALYSIS ---")

print(
    group_analysis(
        df,
        "Pclass",
        "Fare",
    )
)


print("\n--- CORRELATION ---")

print(
    correlation_analysis(
        df,
        "Age",
        "Fare",
        method="pearson",
    )
)


print("\n--- CHI-SQUARE TEST ---")

print(
    hypothesis_test(
        df,
        test="chi_square",
        column="Survived",
        group_column="Sex",
    )
)


print("\n--- T-TEST ---")

print(
    hypothesis_test(
        df,
        test="t_test",
        column="Age",
        group_column="Survived",
    )
)