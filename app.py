import streamlit as st

from whisper_module import (
    start_recording,
    stop_recording,
    transcribe_audio
)

from transcript_analyzer import (
    analyze_transcript
)

from perplexity_engine import (
    calculate_perplexity
)

from scoring_engine import (
    calculate_preparedness_score
)

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

</style>
""", unsafe_allow_html=True)

# =====================================
# SESSION STATE
# =====================================

if "recording" not in st.session_state:
    st.session_state.recording = False

if "audio_saved" not in st.session_state:
    st.session_state.audio_saved = False

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

        st.success(
            "Recording"
        )

    else:

        st.info(
            "Idle"
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
    
    elif response_type == "Prepared Response":
        badge_color = "#F59E0B"
    
    else:
        badge_color = "#EA580C"
        
    st.markdown(
        f"""
        <div style="
        background:white;
        border:1px solid #E7E2DA;
        border-radius:20px;
        padding:20px;
        ">
        
        <h2 style="
        margin:0;
        color:{badge_color};
        ">
        {response_type}
        </h2>
        
        <h1 style="
        font-size:48px;
        margin-top:15px;
        margin-bottom:10px;
        color:#2D2D2D;
        ">
        
        {result['preparedness_score']:.0f}/100
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