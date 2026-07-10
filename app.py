import streamlit as st

from datetime import datetime

import uuid

from evaluation.evaluation_logger import save_evaluation

from modules.whisper_module import (
    start_recording,
    stop_recording,
    transcribe_audio
)

from modules.transcript_analyzer import (
    analyze_transcript
)
from modules.perplexity_engine import (
    calculate_perplexity
)
from modules.preparedness_engine import (
    calculate_preparedness_score
)

from modules.knowledge_retriever import KnowledgeRetriever
from modules.similarity_engine import SimilarityEngine
from modules.plagiarism_engine import PlagiarismEngine
from modules.baseline_engine import generate_candidate_baseline
from modules.outlier_engine import detect_outlier
from modules.ai_detection_engine import detect_ai_generated_response
from modules.authenticity_engine import AuthenticityEngine

from modules.interview_session_engine import (
    create_session,
    add_response,
    generate_summary,
    save_session
)

from modules.interview_models import InterviewResponse

# =====================================
# ENGINE INITIALIZATION
# =====================================

retriever = KnowledgeRetriever()

similarity_engine = SimilarityEngine()

plagiarism_engine = PlagiarismEngine()

authenticity_engine = AuthenticityEngine()
# =====================================
# PAGE CONFIG
# =====================================

st.set_page_config(
    page_title="Interview Transcript Intelligence",
    layout="wide"
)

# =====================================
# CUSTOM CSS
# =====================================

st.markdown("""
<style>

.stApp{
    background-color:#F7F5F2;
}

.block-container{
    max-width:1300px;
    padding-top:2rem;
    padding-bottom:2rem;
}

.hero-card{
    background:white;
    border:1px solid #E7E2DA;
    border-radius:20px;
    padding:35px;
    margin-bottom:25px;
}

.section-card{
    background:white;
    border:1px solid #E7E2DA;
    border-radius:16px;
    padding:20px;
}

div[data-testid="stMetric"]{
    background:white;
    border:1px solid #E7E2DA;
    border-radius:16px;
    padding:18px;
}

header{
    visibility:hidden;
}

[data-testid="stHeader"]{
    background:transparent;
}

.stButton button{
    border-radius:12px;
    height:50px;
}

</style>
""", unsafe_allow_html=True)

# =====================================
# SESSION STATE
# =====================================

if "recording" not in st.session_state:
    st.session_state.recording = False

if "audio_saved" not in st.session_state:
    st.session_state.audio_saved = False

if "interview_session" not in st.session_state:
    st.session_state.interview_session = None

if "candidate_name" not in st.session_state:
    st.session_state.candidate_name = ""

if "question_number" not in st.session_state:
    st.session_state.question_number = 1
    
# =====================================
# HERO SECTION
# =====================================

st.markdown("""
<div class="hero-card">

<h1 style="
margin-bottom:10px;
color:#2D2D2D;
">
Interview Transcript Intelligence
</h1>

<p style="
font-size:18px;
color:#666;
">
Real-time linguistic assessment of spoken interview responses using
speech recognition, language modeling, and transcript analytics.
</p>

</div>
""", unsafe_allow_html=True)

# =====================================
# INTERVIEW SETUP
# =====================================

st.divider()

st.subheader("Interview Setup")

left, right = st.columns([2, 2])

with left:

    candidate_name = st.text_input(
        "Candidate Name",
        value=st.session_state.candidate_name,
        placeholder="Enter candidate name..."
    )

    st.session_state.candidate_name = candidate_name

with right:

    interview_question = st.text_area(
        "Interview Question",
        placeholder="Enter the interview question..."
    )

    ground_truth = st.selectbox(

        "Ground Truth (Evaluation Only)",

        [

            "Genuine",

            "AI",

            "Wikipedia"

        ],

        help="Used only for evaluation. It does not influence the prediction."

    )
    
if st.session_state.interview_session is None:

    start_interview = st.button(

        "Start Interview",

        type="primary",

        use_container_width=True

    )

    if start_interview:

        if candidate_name.strip() == "":

            st.warning(
                "Please enter the candidate name."
            )

            st.stop()

        st.session_state.interview_session = create_session(

            candidate_name=candidate_name,

            interview_id=(

                datetime.now().strftime("%Y%m%d_%H%M%S")

                + "_"

                + uuid.uuid4().hex[:6]

            )

        )

        st.success(

            "Interview session created successfully."

        )

else:

    st.success("🟢 Interview in Progress")

    st.info(

        f"""
Candidate: **{st.session_state.interview_session.candidate_name}**

Questions Answered: **{len(st.session_state.interview_session.responses)}**
"""

    )
     
# =====================================
# RECORDING CONTROLS
# =====================================

controls_col, status_col = st.columns([2,1])

with controls_col:

    st.subheader("Recording Controls")

    c1, c2, c3 = st.columns(3)

    with c1:

        if st.button("Start Recording"):

            start_recording()

            st.session_state.recording = True

    with c2:

        if st.button("Stop Recording"):

            stop_recording()

            st.session_state.recording = False

            st.session_state.audio_saved = True

    with c3:

        analyze_button = st.button(
            "Analyze Response"
        )
        
with status_col:

    st.subheader("Status")

    if st.session_state.recording:

        st.error(
            "● Recording"
        )

    elif st.session_state.audio_saved:

        st.success(
            "● Ready for Analysis"
        )

    else:

        st.info(
            "● Awaiting Recording"
        )

# =====================================
# ANALYSIS
# =====================================

if analyze_button:

    if not st.session_state.audio_saved:

        st.warning(
            "Please record audio first."
        )

        st.stop()

    # ================================
    # WHISPER
    # ================================

    with st.spinner(
        "Transcribing audio..."
    ):

        transcript = transcribe_audio()

    # ================================
    # NLP ANALYSIS
    # ================================

    metrics = analyze_transcript(
        transcript
    )

    MIN_WORDS = 20

    if metrics["total_words"] < MIN_WORDS:

        st.warning(
            f"""
        Transcript too short for reliable analysis.
        Words Detected:
        {metrics['total_words']}
        Minimum Required:
        {MIN_WORDS}
       """
        )

        st.stop()

    # ================================
    # PERPLEXITY
    # ================================

    perplexity = calculate_perplexity(
        transcript
    )
    
    metrics["perplexity"] = perplexity

    # ================================
    # PREPAREDNESS SCORING
    # ================================

    result = calculate_preparedness_score(

        total_words=
        metrics["total_words"],

        perplexity=
        perplexity,

        vocabulary_richness=
        metrics["vocabulary_richness"],

        sentence_consistency=
        metrics["sentence_consistency"],

        repetition_score=
        metrics["repetition_score"],

        formality_score=
        metrics["formality_score"]
    )
    
    # ================================
    # KNOWLEDGE RETRIEVAL
    # ================================
     
    with st.spinner(
        "Retrieving reference documents..."
    ):
        retrieved_documents = retriever.retrieve(
            
            interview_question
        )
    
    st.success(
        f"Retrieved {len(retrieved_documents)} reference document(s)."
    )
    
    # ================================
    # SIMILARITY ANALYSIS
    # ================================
    
    with st.spinner(
        "Computing similarity..."
    ):
        similarity_results = similarity_engine.compare(
            
            transcript,
            
            retrieved_documents
        )
    
    st.success(

    f"Computed similarity against {len(similarity_results)} document(s)."
    )
    
    # ================================
    # PLAGIARISM ANALYSIS
    # ================================

    with st.spinner(
        "Evaluating plagiarism..."
        ):
        
        plagiarism_result = plagiarism_engine.assess(
            
            similarity_results
        )

    st.success(
        "Plagiarism analysis completed."
    )
    
    # ================================
    # BASELINE GENERATION
    # ================================

    baseline = generate_candidate_baseline(
        
        st.session_state.interview_session

    )

    if baseline is None:

        st.info(
            "Building candidate baseline..."
        )

    else:

        st.success(

            f"Baseline built from {baseline['responses_used']} response(s)."

        )
    
    # ================================
    # OUTLIER DETECTION
    # ================================

    outlier_result = None

    if baseline is not None:

        outlier_result = detect_outlier(

            metrics,

            baseline

        )

        st.success(

            "Outlier detection completed."

        )

    else:

        st.info(

            "Outlier detection skipped (baseline unavailable)."

        )
    
    # ================================
    # AI DETECTION
    # ================================

    with st.spinner(
        "Detecting AI-generated response..."
    ):
        ai_result = detect_ai_generated_response(
            
            perplexity=perplexity,

            vocabulary_richness=metrics["vocabulary_richness"],

            sentence_consistency=metrics["sentence_consistency"],

            repetition_score=metrics["repetition_score"],

            formality_score=metrics["formality_score"],

            preparedness_score=result["preparedness_score"],

            plagiarism_score=plagiarism_result.plagiarism_score,

            is_outlier=(
                False
                if outlier_result is None
                else outlier_result["is_outlier"]
            )
        )
    st.success(
        "AI detection completed."
    )
    
    # ================================
    # AUTHENTICITY ENGINE
    # ================================

    with st.spinner(
        "Computing authenticity score..."
    ):

        authenticity_result = authenticity_engine.assess(

            preparedness_score=result["preparedness_score"],

            plagiarism_score=plagiarism_result.plagiarism_score,

            outlier_flag=(
                False
                if outlier_result is None
                else outlier_result["is_outlier"]
            ),

            ai_probability=ai_result["ai_probability"]

        )

    st.success(
        "Authenticity assessment completed."
    )
    
    # ================================
    # SAVE RESPONSE TO INTERVIEW
    # ================================

    add_response(
        
        session=st.session_state.interview_session,
        
        question=interview_question,

        answer=transcript,

        metrics=metrics,

        preparedness=result,

        similarity=vars(plagiarism_result),

        baseline_deviation=outlier_result,

        ai_flag=ai_result,

        authenticity=vars(authenticity_result),
        
        retrieved_documents=retrieved_documents

    )
    
    st.session_state.interview_session.baseline = generate_candidate_baseline(
        st.session_state.interview_session
    )
    
    # =====================================
    # PREDICT RESPONSE TYPE
    # =====================================

    ai_probability = ai_result["ai_probability"]

    plagiarism_score = plagiarism_result.plagiarism_score

    if ai_probability >= 70 and plagiarism_score >= 70:
        
        prediction = "Hybrid AI + Copy"

    elif plagiarism_score >= 70:
        
        prediction = "Wikipedia"

    elif ai_probability >= 70:

        prediction = "AI"

    else:

        prediction = "Genuine"
    
    save_evaluation(

        candidate=st.session_state.interview_session.candidate_name,

        question=interview_question,

        ground_truth=ground_truth,

        prediction=prediction,

        ai_probability=ai_probability,

        plagiarism_score=plagiarism_score,

        authenticity_score=authenticity_result.authenticity_score

    )

    # ================================
    # TRANSCRIPT
    # ================================

    st.divider()

    st.subheader(
    "Transcript"
    )
    
    with st.container(border=True):
        st.write(
            transcript
        )

    # ================================
    # METRICS
    # ================================

    st.divider()

    st.subheader(
        "Analysis Metrics"
    )

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:

        st.metric(
            "Perplexity",
            round(perplexity, 2)
        )

    with col2:

        st.metric(
            "Vocabulary",
            metrics["vocabulary_richness"]
        )

    with col3:

        st.metric(
            "Consistency",
            metrics["sentence_consistency"]
        )

    with col4:

        st.metric(
            "Repetition",
            metrics["repetition_score"]
        )

    with col5:

        st.metric(
            "Formality",
            metrics["formality_score"]
        )

    # ================================
    # ASSESSMENT
    # ================================

    st.divider()
    
    response_type = result["response_type"]
    
    if response_type == "Natural Response":
        badge_color = "#22C55E"
        card_bg = "#F0FDF4"
        
    elif response_type == "Prepared Response":
        badge_color = "#F59E0B"
        card_bg = "#FFFBEB"
    
    else:
        badge_color = "#EA580C"
        card_bg = "#FFF7ED"
        
    st.markdown(
        f"""
        <div style="
        background:{card_bg};
        border:1px solid #E7E2DA;
        border-radius:20px;
        padding:18px;
        min-height:180px;
        ">
        
        <h2 style="
        margin:0;
        color:{badge_color};
        ">
        {response_type}
        </h2>
        
        <h1 style="
        font-size:42px;
        margin-top:15px;
        margin-bottom:10px;
        color:#2D2D2D;
        ">
        
        {result['preparedness_score']:.0f}
        </h1>
        
        <p style="
        font-size:18px;
        color:#666;
        ">
        Confidence: {result['confidence']:.0f}%
        </p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    
    # ================================
    # CHARACTERISTICS
    # ================================
     
    st.subheader(
        "Key Linguistic Characteristics"
    )
    
    if len(result["observed_traits"]) == 0:
        
        st.write(
            "No strong linguistic characteristics detected."
        )
    else:
        
        cols = st.columns(
            len(result["observed_traits"])
        )
        
        for i, trait in enumerate(
            result["observed_traits"]
        ):
            cols[i].success(
                trait
            )
    
    st.divider()
    
    st.subheader("Plagiarism Analysis")

    col1, col2, col3 = st.columns(3)

    with col1:
        
        st.metric(
            "Plagiarism Score",
            f"{plagiarism_result.plagiarism_score:.1f}%"
    )

    with col2:

        st.metric(
            "Confidence",
            plagiarism_result.confidence
        )

    with col3:

        st.metric(
            "Flagged",
            "Yes" if plagiarism_result.plagiarism_flag else "No"
        )

    st.write("### Best Match")

    st.write(
        f"**Title:** {plagiarism_result.matched_title}"
    )

    st.write(
        f"**Source:** {plagiarism_result.matched_source}"
    )

    st.write(
        f"**Explanation:** {plagiarism_result.explanation}"
    )

    with st.expander("Matched Reference Content"):

        st.write(
            plagiarism_result.matched_content
        )
        
    # =====================================
    # AI DETECTION
    # =====================================

    st.divider()

    st.subheader("AI Detection")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(

            "AI Probability",

            f"{ai_result['ai_probability']:.1f}%"

        )

    with col2:

        st.metric(

            "Confidence",

            f"{ai_result['confidence']:.1f}%"

        )

    with col3:

        st.metric(

            "Risk",

        ai_result["risk_level"]

    )

    st.write("### Recommendation")

    st.info(

        ai_result["recommendation"]

    )

    st.write("### Explanation")

    for item in ai_result["explanation"]:

        st.write(f"• {item}")
        
    st.divider()

    st.subheader("Predicted Response Class")

    if prediction == "Genuine": 

        st.success(f"Prediction: {prediction}")

    elif prediction == "Wikipedia":

        st.warning(f"Prediction: {prediction}")

    elif prediction == "AI":

        st.error(f"Prediction: {prediction}")

    else:

        st.error(f"Prediction: {prediction}")
        
    # =====================================
    # AUTHENTICITY ASSESSMENT
    # =====================================

    st.divider()

    st.subheader("Authenticity Assessment")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(

            "Authenticity Score",

            f"{authenticity_result.authenticity_score:.1f}"

        )

    with col2:

        st.metric(

            "Risk Level",

            authenticity_result.risk_level

        )

    with col3:

        st.metric(

            "Recommendation",

            authenticity_result.recommendation

        )

    st.info(

        authenticity_result.explanation

    )
    
# =====================================================
# FINISH INTERVIEW
# =====================================================

st.divider()

if st.button("Finish Interview"):

    if st.session_state.interview_session is None:

        st.warning("No active interview.")

        st.stop()

    summary = generate_summary(

        st.session_state.interview_session

    )

    filename = save_session(

        st.session_state.interview_session

    )

    st.success("Interview completed successfully.")

    st.success(f"Interview saved to:\n{filename}")

    st.divider()

    st.header("Interview Summary")

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Candidate",
            summary["candidate_name"]
        )

    with col2:

        st.metric(
            "Questions",
            summary["total_questions"]
        )

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Preparedness",
            f"{summary['average_preparedness']:.1f}"
        )

    with col2:

        st.metric(
            "Plagiarism",
            f"{summary['average_plagiarism']:.1f}%"
        )

    with col3:

        st.metric(
            "AI Probability",
            f"{summary['average_ai_probability']:.1f}%"
        )

    with col4:

        st.metric(
            "Authenticity",
            f"{summary['overall_authenticity']:.1f}"
        )

    st.info(
        f"Recommendation: {summary['recommendation']}"
    )

    st.write(
        f"Flagged Questions: {summary['flagged_questions']}"
    )
    
    st.session_state.interview_session = None

    st.session_state.question_number = 1

    st.session_state.audio_saved = False

    st.success(

        "Interview closed. Ready for a new interview."

    )