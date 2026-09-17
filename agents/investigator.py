from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

from tools.statistics import (
    descriptive_statistics,
    group_analysis,
    correlation_analysis,
    hypothesis_test,
)

load_dotenv()


llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0,
)


investigator_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are the Investigator Agent of StatAgent.

Your job is to investigate one analytical task from
an investigation plan.

You have access to statistical tools.

Available tools:

1. descriptive_statistics
   Use for numerical descriptive statistics.

2. group_analysis
   Use to compare a numerical variable across groups.

3. correlation_analysis
   Use to measure relationships between two numerical variables.

4. hypothesis_test
   Use for chi-square, t-test, or Mann-Whitney U tests.

Your job is to determine which tool is appropriate
for the current investigation task.

Do not invent columns.
Only use columns present in the dataset profile.

Return:
- The tool that should be used
- The required columns
- A short explanation of why the tool is appropriate

Do not invent statistical results.
The Python tools will calculate the actual results.
"""
        ),
        (
            "human",
            """
Dataset Profile:
{dataset_profile}

Current Investigation Task:
{current_task}
"""
        ),
    ]
)


def select_analysis_tool(
    dataset_profile: dict,
    current_task: str,
) -> str:

    chain = investigator_prompt | llm

    response = chain.invoke(
        {
            "dataset_profile": dataset_profile,
            "current_task": current_task,
        }
    )

    return response.content