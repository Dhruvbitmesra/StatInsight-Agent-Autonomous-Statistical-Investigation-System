from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()


llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0,
)


report_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are the Final Report Agent of StatAgent.

Your job is to produce a clear analytical report from
the evidence collected during the investigation.

You are given:

1. The user's question
2. The investigation plan
3. Completed investigation tasks
4. Statistical analysis results
5. Critic feedback

Rules:

- Use only the evidence provided.
- Do not invent statistical values.
- Do not perform new calculations.
- Do not claim causation from correlation or association.
- Clearly distinguish statistical evidence from interpretation.
- Mention important limitations when relevant.
- Keep the report concise and understandable.
- Answer the user's original question directly.

Structure the report as:

1. Question
2. Key Findings
3. Statistical Evidence
4. Interpretation
5. Limitations
6. Conclusion
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

Critic Feedback:
{critic_feedback}

Generate the final analytical report.
"""
        ),
    ]
)


def generate_final_report(
    question: str,
    investigation_plan: list[str],
    completed_tasks: list[str],
    analysis_results: list[dict],
    critic_feedback: str,
) -> str:

    chain = report_prompt | llm

    response = chain.invoke(
        {
            "question": question,
            "investigation_plan": investigation_plan,
            "completed_tasks": completed_tasks,
            "analysis_results": analysis_results,
            "critic_feedback": critic_feedback,
        }
    )

    return response.content