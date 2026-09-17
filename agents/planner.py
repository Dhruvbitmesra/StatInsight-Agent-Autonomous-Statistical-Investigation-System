from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os

load_dotenv()


llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0
)


planner_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are the planning agent of StatAgent,
an autonomous statistical investigation system.

Your job is to create a clear investigation plan
for answering the user's analytical question.

You are given:
1. The user's question
2. A profile of the dataset

Create a sequence of analytical tasks that can
provide evidence for answering the question.

Rules:
- Do not perform the analysis yourself.
- Do not invent dataset columns.
- Only use columns available in the dataset profile.
- Prefer statistical and data-driven investigations.
- Break complex questions into smaller tasks.
- Avoid unnecessary analysis.
- Return only a numbered list of investigation tasks.
"""
        ),
        (
            "human",
            """
User Question:
{question}

Dataset Profile:
{dataset_profile}

Create the investigation plan.
"""
        ),
    ]
)


def create_investigation_plan(
    question: str,
    dataset_profile: dict
) -> str:

    chain = planner_prompt | llm

    response = chain.invoke(
        {
            "question": question,
            "dataset_profile": dataset_profile,
        }
    )

    return response.content