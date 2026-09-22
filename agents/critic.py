from pydantic import BaseModel, Field
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()


llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0,
)


class CriticDecision(BaseModel):
    evidence_sufficient: bool = Field(
        description="Whether the collected evidence is sufficient "
                    "to answer the user's question."
    )

    feedback: str = Field(
        description="Short explanation of the decision."
    )


critic_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are the Critic Agent of StatAgent.

Your job is to evaluate whether the completed statistical
investigation provides enough evidence to answer the user's
question.

You are given:
1. The user's question
2. The original investigation plan
3. The completed tasks
4. The statistical analysis results

Rules:

- Do not calculate new statistical results.
- Do not invent evidence.
- Do not perform additional analysis.
- Check whether the completed investigations address the
  user's original question.
- If the evidence is sufficient, mark it as sufficient.
- If important planned tasks remain incomplete, mark it as
  insufficient.
- Give a short explanation.

Return a structured decision.
"""
        ),
        (
            "human",
            """
User Question:
{question}

Investigation Plan:
{investigation_plan}

Completed Tasks:
{completed_tasks}

Analysis Results:
{analysis_results}

Evaluate whether the evidence is sufficient.
"""
        ),
    ]
)


structured_llm = llm.with_structured_output(
    CriticDecision
)


def evaluate_evidence(
    question: str,
    investigation_plan: list[str],
    completed_tasks: list[str],
    analysis_results: list[dict],
) -> CriticDecision:

    chain = critic_prompt | structured_llm

    response = chain.invoke(
        {
            "question": question,
            "investigation_plan": investigation_plan,
            "completed_tasks": completed_tasks,
            "analysis_results": analysis_results,
        }
    )

    return response