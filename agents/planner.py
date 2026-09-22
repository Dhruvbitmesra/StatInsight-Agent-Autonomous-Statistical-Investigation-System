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
# PLANNER PROMPT
# ==================================================

planner_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are the Planning Agent of StatAgent,
an autonomous statistical investigation system.

Your job is to create a small investigation plan
that answers the user's analytical question.

The investigation will be executed by Python tools.

AVAILABLE PYTHON ANALYSIS TOOLS:

1. descriptive_statistics

Purpose:
- Describe ONE numerical variable.
- Can calculate count, mean, median, standard deviation,
  minimum, maximum, Q1 and Q3.

2. group_analysis

Purpose:
- Compare ONE numerical variable across groups.
- Example:
  Compare Age across Survived groups.

3. correlation_analysis

Purpose:
- Measure the relationship between TWO numerical
  variables.
- Supported methods:
  Pearson
  Spearman

4. hypothesis_test

Purpose:
- Test statistical relationships.

Supported tests:

a. chi_square
   - Association between TWO categorical variables.

b. t_test
   - Compare a numerical variable between TWO groups.

c. mann_whitney
   - Non-parametric comparison of a numerical variable
     between TWO groups.

==================================================
STRICT RULES
==================================================

1. Generate ONLY tasks that can be executed by the
   four tools listed above.

2. DO NOT generate tasks involving:

   - data loading
   - data cleaning
   - missing-value handling
   - imputation
   - encoding
   - feature engineering
   - visualization
   - logistic regression
   - linear regression
   - VIF
   - ROC
   - AUC
   - model selection
   - L1/Lasso
   - arbitrary Python code

3. Do not ask Python to modify the dataset.

4. Do not invent columns.

5. Only use columns present in the dataset profile.

6. Generate between 3 and 6 tasks.

7. Every task must correspond to exactly ONE
   supported analysis tool.

8. Every task must be executable directly by the
   Investigator and Executor.

9. Do not create sub-tasks.

10. Do not explain the plan.

11. Return ONLY a numbered list.

==================================================
EXAMPLES
==================================================

For a question such as:

"What factors are associated with passenger survival?"

A valid plan could be:

1. Test the association between Sex and Survived using chi-square.
2. Test the association between Pclass and Survived using chi-square.
3. Compare Age between Survived groups using a t-test.
4. Compare Fare between Survived groups using a t-test.
5. Analyze the correlation between Age and Fare using Pearson correlation.

For:

"What is the relationship between Age and Fare?"

A valid plan could be:

1. Calculate descriptive statistics for Age.
2. Calculate descriptive statistics for Fare.
3. Analyze the Pearson correlation between Age and Fare.

For:

"Does passenger class relate to survival?"

A valid plan could be:

1. Test the association between Pclass and Survived using chi-square.

==================================================
IMPORTANT
==================================================

The dataset profile may contain categorical variables
and missing values.

Do NOT create cleaning tasks.

The dataset is already available to the statistical
tools.

Your job is ONLY to decide which supported statistical
analyses should be performed.
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


# ==================================================
# CREATE INVESTIGATION PLAN
# ==================================================

def create_investigation_plan(
    question: str,
    dataset_profile: dict,
) -> str:

    chain = planner_prompt | llm

    response = chain.invoke(
        {
            "question": question,
            "dataset_profile": dataset_profile,
        }
    )

    return response.content