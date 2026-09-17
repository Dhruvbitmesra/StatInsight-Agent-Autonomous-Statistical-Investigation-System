import pandas as pd
import numpy as np

from scipy.stats import (
    pearsonr,
    spearmanr,
    ttest_ind,
    mannwhitneyu,
    chi2_contingency,
)


def descriptive_statistics(
    df: pd.DataFrame,
    column: str,
) -> dict:

    if column not in df.columns:
        raise ValueError(f"Column '{column}' not found in dataset.")

    if not pd.api.types.is_numeric_dtype(df[column]):
        raise ValueError(
            f"Column '{column}' must be numerical."
        )

    series = df[column].dropna()

    return {
        "column": column,
        "count": int(series.count()),
        "mean": float(series.mean()),
        "median": float(series.median()),
        "std": float(series.std()),
        "min": float(series.min()),
        "max": float(series.max()),
        "q1": float(series.quantile(0.25)),
        "q3": float(series.quantile(0.75)),
    }


def group_analysis(
    df: pd.DataFrame,
    group_column: str,
    value_column: str,
) -> dict:

    if group_column not in df.columns:
        raise ValueError(
            f"Column '{group_column}' not found."
        )

    if value_column not in df.columns:
        raise ValueError(
            f"Column '{value_column}' not found."
        )

    result = (
        df.groupby(group_column)[value_column]
        .agg(["count", "mean", "median"])
        .reset_index()
    )

    return result.to_dict(orient="records")


def correlation_analysis(
    df: pd.DataFrame,
    column1: str,
    column2: str,
    method: str = "pearson",
) -> dict:

    if column1 not in df.columns:
        raise ValueError(f"Column '{column1}' not found.")

    if column2 not in df.columns:
        raise ValueError(f"Column '{column2}' not found.")

    data = df[[column1, column2]].dropna()

    if method == "pearson":
        coefficient, p_value = pearsonr(
            data[column1],
            data[column2],
        )

    elif method == "spearman":
        coefficient, p_value = spearmanr(
            data[column1],
            data[column2],
        )

    else:
        raise ValueError(
            "method must be 'pearson' or 'spearman'."
        )

    return {
        "column1": column1,
        "column2": column2,
        "method": method,
        "correlation": float(coefficient),
        "p_value": float(p_value),
        "sample_size": len(data),
    }


def hypothesis_test(
    df: pd.DataFrame,
    test: str,
    column: str,
    group_column: str | None = None,
) -> dict:

    if column not in df.columns:
        raise ValueError(
            f"Column '{column}' not found."
        )

    if test == "chi_square":

        if group_column is None:
            raise ValueError(
                "group_column is required for chi-square."
            )

        if group_column not in df.columns:
            raise ValueError(
                f"Column '{group_column}' not found."
            )

        contingency_table = pd.crosstab(
            df[group_column],
            df[column],
        )

        statistic, p_value, dof, expected = (
            chi2_contingency(contingency_table)
        )

        return {
            "test": "chi_square",
            "statistic": float(statistic),
            "p_value": float(p_value),
            "degrees_of_freedom": int(dof),
            "sample_size": int(contingency_table.values.sum()),
        }

    if test in {"t_test", "mann_whitney"}:

        if group_column is None:
            raise ValueError(
                "group_column is required."
            )

        if group_column not in df.columns:
            raise ValueError(
                f"Column '{group_column}' not found."
            )

        groups = df[group_column].dropna().unique()

        if len(groups) != 2:
            raise ValueError(
                "The grouping column must contain exactly two groups."
            )

        group1 = df.loc[
            df[group_column] == groups[0],
            column,
        ].dropna()

        group2 = df.loc[
            df[group_column] == groups[1],
            column,
        ].dropna()

        if test == "t_test":

            statistic, p_value = ttest_ind(
                group1,
                group2,
                equal_var=False,
            )

        else:

            statistic, p_value = mannwhitneyu(
                group1,
                group2,
                alternative="two-sided",
            )

        return {
            "test": test,
            "groups": [
                str(groups[0]),
                str(groups[1]),
            ],
            "statistic": float(statistic),
            "p_value": float(p_value),
            "group1_size": len(group1),
            "group2_size": len(group2),
        }

    raise ValueError(
        "Unsupported test. Use "
        "'chi_square', 't_test', or 'mann_whitney'."
    )