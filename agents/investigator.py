from typing import Literal

from pydantic import BaseModel, Field
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()


llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0,
)


class AnalysisDecision(BaseModel):
    tool: Literal[
        "descriptive_statistics",
        "group_analysis",
        "correlation_analysis",
        "hypothesis_test",
    ] = Field(
        description="The statistical tool that should be used."
    )

    column: str = Field(
        description="Primary column required for the analysis."
    )

    second_column: str | None = Field(
        default=None,
        description="Second column if required."
    )

    group_column: str | None = Field(
        default=None,
        description="Grouping column if required."
    )

    test: str | None = Field(
        default=None,
        description="Statistical test if hypothesis_test is selected."
    )

    reason: str = Field(
        description="Short explanation for selecting the tool."
    )


investigator_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are the Investigator Agent of StatAgent.

Your job is to select the correct statistical analysis
for one investigation task.

Available tools:

1. descriptive_statistics
   For describing one numerical variable.

2. group_analysis
   For comparing a numerical variable across groups.

3. correlation_analysis
   For measuring the relationship between two numerical
   variables.

4. hypothesis_test
   Supports:
   - chi_square
   - t_test
   - mann_whitney

Rules:

- Only use columns present in the dataset profile.
- Do not invent columns.
- Do not calculate statistical results yourself.
- Select only one tool.
- If hypothesis_test is selected, specify the appropriate test.
- Return a structured analysis decision.
"""
        ),
        (
            "human",
            """
Dataset Profile:
{dataset_profile}

Current Investigation Task:
{current_task}

Select the appropriate statistical analysis.
"""
        ),
    ]
)


structured_llm = llm.with_structured_output(
    AnalysisDecision
)


def select_analysis_tool(
    dataset_profile: dict,
    current_task: str,
) -> AnalysisDecision:

    chain = investigator_prompt | structured_llm

    response = chain.invoke(
        {
            "dataset_profile": dataset_profile,
            "current_task": current_task,
        }
    )

    return response