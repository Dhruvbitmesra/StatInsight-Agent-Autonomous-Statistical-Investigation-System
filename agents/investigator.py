from typing import Literal

from pydantic import BaseModel, Field

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

from dotenv import load_dotenv

load_dotenv()


# ==================================================
# LLM
# ==================================================

llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0,
)


# ==================================================
# STRUCTURED DECISION
# ==================================================

class AnalysisDecision(BaseModel):

    tool: Literal[
        "descriptive_statistics",
        "group_analysis",
        "correlation_analysis",
        "hypothesis_test",
    ] = Field(
        description=(
            "Statistical tool to execute."
        )
    )

    column: str = Field(
        description=(
            "Primary column for the analysis. "
            "For chi-square this should be the "
            "outcome/second categorical variable."
        )
    )

    second_column: str | None = Field(
        default=None,
        description=(
            "Second numerical column for "
            "correlation analysis."
        )
    )

    group_column: str | None = Field(
        default=None,
        description=(
            "Grouping or first categorical column. "
            "For chi-square this MUST contain the "
            "other categorical variable."
        )
    )

    test: str | None = Field(
        default=None,
        description=(
            "Statistical test when using "
            "hypothesis_test."
        )
    )

    reason: str = Field(
        description=(
            "Short explanation for selecting "
            "the analysis."
        )
    )


# ==================================================
# INVESTIGATOR PROMPT
# ==================================================

investigator_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are the Investigator Agent of StatAgent.

Your job is to convert ONE investigation task
into a structured statistical analysis decision.

AVAILABLE TOOLS:

1. descriptive_statistics

Use when the task asks for summary statistics
of ONE numerical column.

Required:
- column

Example:
"Calculate descriptive statistics for Age."

Decision:
tool = descriptive_statistics
column = Age


2. group_analysis

Use when comparing ONE numerical variable
across groups.

Required:
- column = numerical variable
- group_column = grouping variable

Example:
"Compare Age across Survived groups."

Decision:
tool = group_analysis
column = Age
group_column = Survived


3. correlation_analysis

Use when measuring the relationship between
TWO numerical variables.

Required:
- column = first numerical variable
- second_column = second numerical variable

Example:
"Analyze the correlation between Age and Fare."

Decision:
tool = correlation_analysis
column = Age
second_column = Fare


4. hypothesis_test

Use for hypothesis testing.

Supported tests:

A. chi_square

Use for association between TWO categorical
variables.

Required:
- column = outcome/second categorical variable
- group_column = first categorical variable
- test = chi_square

IMPORTANT:
For a task like:

"Test the association between Sex and Survived
using chi-square."

you MUST return:

tool = hypothesis_test
column = Survived
group_column = Sex
test = chi_square

Both columns are required.

B. t_test

Use to compare ONE numerical variable
between TWO groups.

Required:
- column = numerical variable
- group_column = grouping variable
- test = t_test

Example:

"Compare Age between Survived groups."

Return:

tool = hypothesis_test
column = Age
group_column = Survived
test = t_test


C. mann_whitney

Use when the task explicitly requests
Mann-Whitney or a non-parametric comparison.

Required:
- column
- group_column
- test = mann_whitney


==================================================
STRICT RULES
==================================================

1. Only use columns present in the dataset profile.

2. Never invent column names.

3. Do not perform the statistical calculation.

4. Return exactly ONE analysis decision.

5. For chi_square:
   - group_column MUST be populated.
   - column MUST be populated.
   - test MUST be "chi_square".

6. For t_test:
   - group_column MUST be populated.
   - column MUST be populated.
   - test MUST be "t_test".

7. For mann_whitney:
   - group_column MUST be populated.
   - column MUST be populated.
   - test MUST be "mann_whitney".

8. For correlation_analysis:
   - column MUST be populated.
   - second_column MUST be populated.

9. For group_analysis:
   - column MUST be populated.
   - group_column MUST be populated.

10. For descriptive_statistics:
    - column MUST be populated.

Return only the structured decision.
"""
        ),
        (
            "human",
            """
Dataset Profile:

{dataset_profile}


Current Investigation Task:

{current_task}


Select the correct statistical analysis.
"""
        ),
    ]
)


# ==================================================
# STRUCTURED LLM
# ==================================================

structured_llm = llm.with_structured_output(
    AnalysisDecision
)


# ==================================================
# SELECT ANALYSIS TOOL
# ==================================================

def select_analysis_tool(
    dataset_profile: dict,
    current_task: str,
) -> AnalysisDecision:

    chain = (
        investigator_prompt
        | structured_llm
    )

    response = chain.invoke(
        {
            "dataset_profile":
                dataset_profile,

            "current_task":
                current_task,
        }
    )

    return response