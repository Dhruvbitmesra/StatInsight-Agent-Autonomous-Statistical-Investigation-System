import streamlit as st
import pandas as pd
import tempfile
from pathlib import Path

from graph.workflow import workflow


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="StatAgent",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# CUSTOM CSS
# NO RAW HTML IS USED FOR THE UI
# ============================================================

st.markdown(
    """
    <style>

    /* ========================================================
       APP BACKGROUND
       ======================================================== */

    .stApp {
        background:
            radial-gradient(
                circle at 8% 10%,
                rgba(99, 102, 241, 0.18),
                transparent 28%
            ),
            radial-gradient(
                circle at 92% 15%,
                rgba(6, 182, 212, 0.12),
                transparent 30%
            ),
            radial-gradient(
                circle at 50% 100%,
                rgba(139, 92, 246, 0.13),
                transparent 35%
            ),
            #070914;

        color: #f8fafc;

        min-height: 100vh;
    }


    /* ========================================================
       WAVING BACKGROUND
       Created entirely with pseudo-elements
       ======================================================== */

    .stApp::before {
        content: "";

        position: fixed;

        left: -10%;
        bottom: -190px;

        width: 120%;
        height: 360px;

        background:
            linear-gradient(
                90deg,
                rgba(99, 102, 241, 0.14),
                rgba(139, 92, 246, 0.18),
                rgba(6, 182, 212, 0.12),
                rgba(99, 102, 241, 0.14)
            );

        border-radius: 50% 50% 0 0;

        filter: blur(20px);

        transform: rotate(-2deg);

        animation:
            waveOne 12s ease-in-out infinite alternate;

        pointer-events: none;

        z-index: 0;
    }


    .stApp::after {
        content: "";

        position: fixed;

        left: -10%;
        bottom: -230px;

        width: 120%;
        height: 360px;

        background:
            linear-gradient(
                90deg,
                rgba(6, 182, 212, 0.10),
                rgba(99, 102, 241, 0.13),
                rgba(236, 72, 153, 0.08)
            );

        border-radius: 50% 50% 0 0;

        filter: blur(24px);

        transform: rotate(2deg);

        animation:
            waveTwo 17s ease-in-out infinite alternate;

        pointer-events: none;

        z-index: 0;
    }


    @keyframes waveOne {

        0% {
            transform:
                translateX(-4%)
                rotate(-3deg)
                scaleY(0.9);
        }

        50% {
            transform:
                translateX(3%)
                rotate(1deg)
                scaleY(1.1);
        }

        100% {
            transform:
                translateX(-2%)
                rotate(-1deg)
                scaleY(0.95);
        }
    }


    @keyframes waveTwo {

        0% {
            transform:
                translateX(4%)
                rotate(2deg)
                scaleY(1);
        }

        50% {
            transform:
                translateX(-3%)
                rotate(-1deg)
                scaleY(1.12);
        }

        100% {
            transform:
                translateX(2%)
                rotate(2deg)
                scaleY(0.94);
        }
    }


    /* ========================================================
       CONTENT LAYER
       ======================================================== */

    .block-container {
        position: relative;

        z-index: 2;

        padding-top: 2rem;
        padding-bottom: 5rem;
    }


    /* ========================================================
       HERO
       ======================================================== */

    .hero-title {
        text-align: center !important;

        font-size: 4.5rem !important;

        font-weight: 800 !important;

        letter-spacing: -0.055em !important;

        margin-top: 0.4rem !important;

        margin-bottom: 0.3rem !important;

        background:
            linear-gradient(
                90deg,
                #ffffff,
                #c7d2fe,
                #67e8f9,
                #ffffff
            );

        background-size: 250% auto;

        -webkit-background-clip: text;

        -webkit-text-fill-color: transparent;

        animation:
            titleGradient 7s linear infinite;
    }


    @keyframes titleGradient {

        0% {
            background-position: 0% center;
        }

        100% {
            background-position: 250% center;
        }
    }


    .hero-subtitle {
        text-align: center !important;

        max-width: 720px;

        margin-left: auto;
        margin-right: auto;

        color: #94a3b8 !important;

        font-size: 1.05rem !important;

        line-height: 1.7 !important;
    }


    /* ========================================================
       BADGE
       ======================================================== */

    .badge-container {
        text-align: center;

        margin-top: 1rem;
        margin-bottom: 0.8rem;
    }


    /* ========================================================
       GLASS CONTAINERS
       ======================================================== */

    div[data-testid="stVerticalBlockBorderWrapper"] {

        background:
            linear-gradient(
                135deg,
                rgba(255, 255, 255, 0.055),
                rgba(255, 255, 255, 0.018)
            );

        border:
            1px solid
            rgba(255, 255, 255, 0.08);

        border-radius: 22px;

        backdrop-filter: blur(18px);

        -webkit-backdrop-filter: blur(18px);

        box-shadow:
            0 20px 60px
            rgba(0, 0, 0, 0.20);

        padding: 0.4rem;
    }


    /* ========================================================
       HEADINGS
       ======================================================== */

    .section-heading {
        color: #f8fafc;

        font-size: 1.15rem;

        font-weight: 700;

        margin-bottom: 0.25rem;
    }


    .section-description {
        color: #64748b;

        font-size: 0.88rem;

        line-height: 1.6;

        margin-bottom: 1rem;
    }


    /* ========================================================
       PIPELINE
       ======================================================== */

    .pipeline-box {
        background:
            rgba(255, 255, 255, 0.025);

        border:
            1px solid
            rgba(255, 255, 255, 0.06);

        border-radius: 20px;

        padding: 1rem;

        margin-top: 0.5rem;
        margin-bottom: 1.5rem;
    }


    /* ========================================================
       FILE UPLOADER
       ======================================================== */

    [data-testid="stFileUploader"] {

        background:
            rgba(255, 255, 255, 0.025);

        border:
            1px dashed
            rgba(129, 140, 248, 0.30);

        border-radius: 16px;

        padding: 0.5rem;

        transition:
            all 0.25s ease;
    }


    [data-testid="stFileUploader"]:hover {

        border-color:
            rgba(129, 140, 248, 0.65);

        background:
            rgba(99, 102, 241, 0.045);
    }


    /* ========================================================
       TEXT AREA
       ======================================================== */

    textarea {

        background:
            rgba(255, 255, 255, 0.035) !important;

        border:
            1px solid
            rgba(255, 255, 255, 0.09) !important;

        border-radius:
            14px !important;

        color:
            #f8fafc !important;

        font-size:
            0.95rem !important;
    }


    textarea:focus {

        border-color:
            rgba(129, 140, 248, 0.60) !important;

        box-shadow:
            0 0 0 1px
            rgba(129, 140, 248, 0.20) !important;
    }


    /* ========================================================
       BUTTON
       ======================================================== */

    .stButton > button {

        width: 100%;

        min-height: 52px;

        border-radius: 14px;

        border:
            1px solid
            rgba(129, 140, 248, 0.30);

        background:
            linear-gradient(
                135deg,
                #6366f1,
                #8b5cf6
            );

        color: white;

        font-size: 0.95rem;

        font-weight: 700;

        box-shadow:
            0 10px 30px
            rgba(99, 102, 241, 0.20);

        transition:
            all 0.25s ease;
    }


    .stButton > button:hover {

        transform:
            translateY(-2px);

        border-color:
            rgba(255, 255, 255, 0.35);

        box-shadow:
            0 16px 40px
            rgba(99, 102, 241, 0.38);
    }


    /* ========================================================
       METRICS
       ======================================================== */

    div[data-testid="stMetric"] {

        background:
            rgba(255, 255, 255, 0.035);

        border:
            1px solid
            rgba(255, 255, 255, 0.07);

        border-radius: 16px;

        padding: 0.8rem;

        transition:
            all 0.25s ease;
    }


    div[data-testid="stMetric"]:hover {

        transform:
            translateY(-3px);

        border-color:
            rgba(129, 140, 248, 0.35);
    }


    div[data-testid="stMetricLabel"] {

        color: #64748b !important;
    }


    div[data-testid="stMetricValue"] {

        color: #f8fafc !important;
    }


    /* ========================================================
       EXPANDERS
       ======================================================== */

    div[data-testid="stExpander"] {

        background:
            rgba(255, 255, 255, 0.025);

        border:
            1px solid
            rgba(255, 255, 255, 0.07);

        border-radius: 15px;
    }


    /* ========================================================
       DATAFRAME
       ======================================================== */

    div[data-testid="stDataFrame"] {

        border-radius: 14px;

        overflow: hidden;

        border:
            1px solid
            rgba(255, 255, 255, 0.07);
    }


    /* ========================================================
       SIDEBAR
       ======================================================== */

    section[data-testid="stSidebar"] {

        background:
            rgba(7, 9, 20, 0.94);

        border-right:
            1px solid
            rgba(255, 255, 255, 0.06);
    }


    /* ========================================================
       SIDEBAR LOGO
       ======================================================== */

    .sidebar-title {
        font-size: 1.4rem;

        font-weight: 800;

        color: #c7d2fe;
    }


    /* ========================================================
       FOOTER
       ======================================================== */

    .footer-text {

        text-align: center;

        color: #475569;

        font-size: 0.75rem;

        margin-top: 2rem;
    }


    /* ========================================================
       STREAMLIT CLEANUP
       ======================================================== */

    #MainMenu {
        visibility: hidden;
    }


    footer {
        visibility: hidden;
    }


    header {
        background: transparent !important;
    }


    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        '<div class="sidebar-title">◈ StatAgent</div>',
        unsafe_allow_html=True,
    )

    st.caption(
        "Autonomous Data Investigation"
    )

    st.divider()

    st.markdown(
        "### How it works"
    )

    st.markdown(
        """
        **01** · Profile your dataset

        **02** · Build an investigation plan

        **03** · Select statistical tools

        **04** · Execute deterministic analysis

        **05** · Validate the evidence

        **06** · Generate the report
        """
    )

    st.divider()

    st.markdown(
        "### Powered by"
    )

    st.caption(
        "LangGraph · LangChain · Groq"
    )

    st.caption(
        "Pandas · SciPy · Python"
    )

    st.divider()

    st.caption(
        "StatAgent MVP"
    )


# ============================================================
# HERO
# ============================================================

st.markdown(
    '<div class="badge-container">',
    unsafe_allow_html=True,
)

st.info(
    "✦  AUTONOMOUS STATISTICAL INTELLIGENCE"
)

st.markdown(
    "</div>",
    unsafe_allow_html=True,
)


st.markdown(
    '<h1 class="hero-title">StatAgent</h1>',
    unsafe_allow_html=True,
)


st.markdown(
    """
    <p class="hero-subtitle">
        Turn a dataset and a natural-language question
        into an evidence-backed statistical investigation.
        Let the agent plan, analyze, validate, and explain.
    </p>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# PIPELINE
# ============================================================

pipeline_columns = st.columns(
    [1.2, 0.25, 1.2, 0.25, 1.4, 0.25, 1.4, 0.25, 1.1, 0.25, 1.1]
)


pipeline_items = [
    ("Dataset", 0),
    ("→", 1),
    ("Planner", 2),
    ("→", 3),
    ("Investigator", 4),
    ("→", 5),
    ("Python Tools", 6),
    ("→", 7),
    ("Critic", 8),
    ("→", 9),
    ("Report", 10),
]


for text, index in pipeline_items:

    with pipeline_columns[index]:

        if text == "→":

            st.markdown(
                f"""
                <div style="
                    text-align:center;
                    color:#475569;
                    padding-top:8px;
                    font-size:18px;
                ">
                    {text}
                </div>
                """,
                unsafe_allow_html=True,
            )

        else:

            st.markdown(
                f"""
                <div style="
                    text-align:center;
                    padding:9px 10px;
                    border-radius:999px;
                    background:rgba(99,102,241,0.08);
                    border:1px solid rgba(129,140,248,0.20);
                    color:#c7d2fe;
                    font-size:12px;
                    font-weight:600;
                ">
                    {text}
                </div>
                """,
                unsafe_allow_html=True,
            )


# ============================================================
# DATASET UPLOAD
# ============================================================

with st.container(border=True):

    st.markdown(
        '<div class="section-heading">'
        '01 · Upload your dataset'
        '</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="section-description">'
        'Start with a CSV file. StatAgent will inspect its '
        'structure before deciding how to investigate your question.'
        '</div>',
        unsafe_allow_html=True,
    )

    uploaded_file = st.file_uploader(
        "Drop your CSV here",
        type=["csv"],
        label_visibility="collapsed",
    )


# ============================================================
# DATASET OVERVIEW
# ============================================================

if uploaded_file is not None:

    try:

        df = pd.read_csv(
            uploaded_file
        )

    except Exception as e:

        st.error(
            f"Could not read the CSV file: {e}"
        )

        st.stop()


    with st.container(border=True):

        st.markdown(
            '<div class="section-heading">'
            'Dataset overview'
            '</div>',
            unsafe_allow_html=True,
        )

        col1, col2, col3, col4 = st.columns(4)


        with col1:

            st.metric(
                "Rows",
                f"{len(df):,}",
            )


        with col2:

            st.metric(
                "Columns",
                len(df.columns),
            )


        with col3:

            st.metric(
                "Missing values",
                f"{int(df.isnull().sum().sum()):,}",
            )


        with col4:

            numeric_count = len(
                df.select_dtypes(
                    include="number"
                ).columns
            )

            st.metric(
                "Numeric fields",
                numeric_count,
            )


        with st.expander(
            "Preview dataset"
        ):

            st.dataframe(
                df.head(10),
                use_container_width=True,
            )


# ============================================================
# QUESTION
# ============================================================

with st.container(border=True):

    st.markdown(
        '<div class="section-heading">'
        '02 · What do you want to investigate?'
        '</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="section-description">'
        'Ask a business, research, or statistical question '
        'in plain English.'
        '</div>',
        unsafe_allow_html=True,
    )

    question = st.text_area(
        "Question",
        placeholder=(
            "Example: What factors are associated "
            "with passenger survival?"
        ),
        height=110,
        label_visibility="collapsed",
    )


# ============================================================
# RUN BUTTON
# ============================================================

run_button = st.button(
    "✦  Run Investigation",
    type="primary",
    use_container_width=True,
)


# ============================================================
# EXECUTION
# ============================================================

if run_button:

    if uploaded_file is None:

        st.warning(
            "Please upload a CSV dataset first."
        )

        st.stop()


    if not question.strip():

        st.warning(
            "Please enter an analytical question first."
        )

        st.stop()


    # --------------------------------------------------------
    # TEMPORARY DATASET
    # --------------------------------------------------------

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".csv",
    ) as temp_file:

        temp_file.write(
            uploaded_file.getvalue()
        )

        dataset_path = temp_file.name


    initial_state = {
        "question": question.strip(),
        "dataset_path": dataset_path,
    }


    # --------------------------------------------------------
    # PROGRESS
    # --------------------------------------------------------

    st.divider()

    st.subheader(
        "◈ Agent Investigation"
    )

    progress = st.progress(0)

    status = st.empty()


    try:

        status.info(
            "Initializing StatAgent..."
        )

        progress.progress(10)


        status.info(
            "Profiling dataset..."
        )

        progress.progress(20)


        status.info(
            "Planning investigation..."
        )

        progress.progress(30)


        status.info(
            "Selecting statistical tools..."
        )

        progress.progress(45)


        status.info(
            "Executing statistical analysis..."
        )

        progress.progress(65)


        # ----------------------------------------------------
        # WORKFLOW
        # ----------------------------------------------------

        result = workflow.invoke(
            initial_state
        )


        progress.progress(85)


        status.info(
            "Validating evidence and generating report..."
        )


        progress.progress(100)


        status.success(
            "Investigation completed successfully."
        )


        # ====================================================
        # PLAN
        # ====================================================

        with st.container(border=True):

            st.subheader(
                "03 · Investigation Plan"
            )

            st.caption(
                "Tasks generated by the Planner Agent."
            )


            plan = result.get(
                "investigation_plan",
                [],
            )


            for index, task in enumerate(
                plan,
                start=1,
            ):

                st.markdown(
                    f"""
                    **{index}.** {task}
                    """
                )


        # ====================================================
        # RESULTS
        # ====================================================

        with st.container(border=True):

            st.subheader(
                "04 · Statistical Evidence"
            )

            st.caption(
                "Results calculated deterministically "
                "using Python statistical tools."
            )


            analysis_results = result.get(
                "analysis_results",
                [],
            )


            for index, item in enumerate(
                analysis_results,
                start=1,
            ):

                tool = item.get(
                    "tool",
                    "analysis",
                )


                with st.expander(
                    f"Analysis {index}  ·  {tool}",
                    expanded=True,
                ):

                    st.write(
                        "**Investigation task**"
                    )

                    st.write(
                        item.get(
                            "task",
                            "",
                        )
                    )

                    st.write(
                        "**Statistical result**"
                    )

                    st.json(
                        item.get(
                            "analysis",
                            {},
                        )
                    )


        # ====================================================
        # CRITIC
        # ====================================================

        with st.container(border=True):

            st.subheader(
                "05 · Evidence Validation"
            )

            st.caption(
                "The Critic Agent evaluates whether "
                "the collected evidence is sufficient."
            )


            evidence_sufficient = result.get(
                "evidence_sufficient",
                False,
            )


            if evidence_sufficient:

                st.success(
                    "✓ Evidence is sufficient."
                )

            else:

                st.warning(
                    "⚠ Evidence may be insufficient."
                )


            critic_feedback = result.get(
                "critic_feedback",
                "",
            )


            if critic_feedback:

                st.info(
                    critic_feedback
                )


        # ====================================================
        # FINAL REPORT
        # ====================================================

        with st.container(border=True):

            st.subheader(
                "06 · Final Analytical Report"
            )

            st.caption(
                "Evidence-backed response generated by StatAgent."
            )


            final_report = result.get(
                "final_report",
                "No report was generated.",
            )


            st.markdown(
                final_report
            )


    except Exception as e:

        status.error(
            "StatAgent encountered an error."
        )

        st.exception(e)


    finally:

        try:

            Path(
                dataset_path
            ).unlink(
                missing_ok=True
            )

        except Exception:

            pass


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "◈ StatAgent · Autonomous Data Investigation System"
)

st.caption(
    "LangGraph · LangChain · Groq · Pandas · SciPy"
)