from tools.statistics import (
    descriptive_statistics,
    group_analysis,
    correlation_analysis,
    hypothesis_test,
)


def execute_analysis(
    df,
    decision,
):
    """
    Execute the statistical tool selected
    by the Investigator Agent.
    """

    if decision.tool == "descriptive_statistics":

        return descriptive_statistics(
            df,
            decision.column,
        )

    if decision.tool == "group_analysis":

        return group_analysis(
            df,
            decision.group_column,
            decision.column,
        )

    if decision.tool == "correlation_analysis":

        return correlation_analysis(
            df,
            decision.column,
            decision.second_column,
        )

    if decision.tool == "hypothesis_test":

        return hypothesis_test(
            df,
            test=decision.test,
            column=decision.column,
            group_column=decision.group_column,
        )

    raise ValueError(
        f"Unsupported analysis tool: {decision.tool}"
    )