"""
==============================================================

AI Detection Engine

Version 2

Rule-based AI-generated response detection.

This module does NOT use an LLM.

Instead, it combines multiple linguistic
features extracted from previous engines.

The objective is to estimate the probability
that an interview response was generated or
read directly from an AI assistant.

==============================================================
"""

from typing import Dict, List

# ==============================================================
# WEIGHTS
# ==============================================================

PERPLEXITY_WEIGHT = 0.20

VOCABULARY_WEIGHT = 0.10

FORMALITY_WEIGHT = 0.10

CONSISTENCY_WEIGHT = 0.10

REPETITION_WEIGHT = 0.10

PREPAREDNESS_WEIGHT = 0.10

PLAGIARISM_WEIGHT = 0.20

OUTLIER_WEIGHT = 0.10

# ==============================================================
# HELPER FUNCTIONS
# ==============================================================

def clamp_score(score: float) -> float:
    """
    Restrict score to the range 0-100.
    """

    return max(0.0, min(100.0, score))


# ==============================================================
# INDIVIDUAL FEATURE SCORING
# ==============================================================

def score_perplexity(perplexity: float):

    score = 0
    explanation = []

    if perplexity < 25:

        score = 100
        explanation.append(
            "Extremely low perplexity (highly predictable text)."
        )

    elif perplexity < 40:

        score = 75
        explanation.append(
            "Low perplexity indicates structured language."
        )

    elif perplexity < 60:

        score = 40
        explanation.append(
            "Moderate perplexity."
        )

    else:

        score = 10
        explanation.append(
            "High perplexity suggests natural variation."
        )

    return score, explanation


def score_vocabulary(vocabulary_richness: float):

    score = 0
    explanation = []

    if vocabulary_richness >= 0.85:

        score = 100
        explanation.append(
            "Very rich vocabulary."
        )

    elif vocabulary_richness >= 0.70:

        score = 70
        explanation.append(
            "Above-average vocabulary richness."
        )

    elif vocabulary_richness >= 0.55:

        score = 40
        explanation.append(
            "Moderate vocabulary richness."
        )

    else:

        score = 10
        explanation.append(
            "Limited vocabulary."
        )

    return score, explanation


def score_formality(formality_score: float):

    score = 0
    explanation = []

    if formality_score >= 0.06:

        score = 100
        explanation.append(
            "Highly formal academic language."
        )

    elif formality_score >= 0.03:

        score = 70
        explanation.append(
            "Formal language detected."
        )

    elif formality_score >= 0.01:

        score = 40
        explanation.append(
            "Some formal expressions used."
        )

    else:

        score = 10
        explanation.append(
            "Mostly conversational language."
        )

    return score, explanation


def score_sentence_consistency(sentence_consistency: float):

    score = 0
    explanation = []

    if sentence_consistency <= 1.5:

        score = 100
        explanation.append(
            "Very uniform sentence lengths."
        )

    elif sentence_consistency <= 3:

        score = 70
        explanation.append(
            "Low sentence variation."
        )

    elif sentence_consistency <= 6:

        score = 40
        explanation.append(
            "Moderate sentence variation."
        )

    else:

        score = 10
        explanation.append(
            "High sentence variation."
        )

    return score, explanation


def score_repetition(repetition_score: float):

    score = 0
    explanation = []

    if repetition_score < 0.05:

        score = 90
        explanation.append(
            "Very little repetition."
        )

    elif repetition_score < 0.12:

        score = 60
        explanation.append(
            "Moderate repetition."
        )

    else:

        score = 20
        explanation.append(
            "Noticeable repeated wording."
        )

    return score, explanation


def score_preparedness(preparedness_score: float):

    score = preparedness_score

    explanation = []

    if preparedness_score >= 80:

        explanation.append(
            "Highly structured response."
        )

    elif preparedness_score >= 60:

        explanation.append(
            "Well-prepared response."
        )

    else:

        explanation.append(
            "Response appears relatively spontaneous."
        )

    return score, explanation


def score_plagiarism(plagiarism_score: float):

    score = plagiarism_score

    explanation = []

    if plagiarism_score >= 75:

        explanation.append(
            "Very high similarity to external sources."
        )

    elif plagiarism_score >= 50:

        explanation.append(
            "Moderate external similarity."
        )

    elif plagiarism_score >= 25:

        explanation.append(
            "Minor overlap with reference material."
        )

    else:

        explanation.append(
            "Minimal overlap with reference documents."
        )

    return score, explanation


def score_outlier(is_outlier: bool):

    if is_outlier:

        return 100, [
            "Response deviates significantly from candidate baseline."
        ]

    return 0, [
        "Response aligns with established candidate baseline."
    ]


# ==============================================================
# WEIGHTED SCORE CALCULATION
# ==============================================================

def calculate_weighted_probability(

    perplexity_score,
    vocabulary_score,
    formality_score,
    consistency_score,
    repetition_score,
    preparedness_score,
    plagiarism_score,
    outlier_score

):

    probability = (

        perplexity_score * PERPLEXITY_WEIGHT +

        vocabulary_score * VOCABULARY_WEIGHT +

        formality_score * FORMALITY_WEIGHT +

        consistency_score * CONSISTENCY_WEIGHT +

        repetition_score * REPETITION_WEIGHT +

        preparedness_score * PREPAREDNESS_WEIGHT +

        plagiarism_score * PLAGIARISM_WEIGHT +

        outlier_score * OUTLIER_WEIGHT

    )

    return round(
        clamp_score(probability),
        2
    )
    
# ==============================================================
# MAIN DETECTION FUNCTION
# ==============================================================

def detect_ai_generated_response(

    perplexity: float,
    vocabulary_richness: float,
    sentence_consistency: float,
    repetition_score: float,
    formality_score: float,
    preparedness_score: float,
    plagiarism_score: float,
    is_outlier: bool

) -> Dict:

    """
    Estimates the probability that a response
    was AI-generated using handcrafted,
    explainable linguistic rules.

    Returns
    -------
    dict

        ai_probability

        confidence

        risk_level

        explanation
    """

    explanations: List[str] = []

    # ----------------------------------------------------------
    # Individual Feature Scores
    # ----------------------------------------------------------

    perplexity_value, notes = score_perplexity(
        perplexity
    )
    explanations.extend(notes)

    vocabulary_value, notes = score_vocabulary(
        vocabulary_richness
    )
    explanations.extend(notes)

    formality_value, notes = score_formality(
        formality_score
    )
    explanations.extend(notes)

    consistency_value, notes = score_sentence_consistency(
        sentence_consistency
    )
    explanations.extend(notes)

    repetition_value, notes = score_repetition(
        repetition_score
    )
    explanations.extend(notes)

    preparedness_value, notes = score_preparedness(
        preparedness_score
    )
    explanations.extend(notes)

    plagiarism_value, notes = score_plagiarism(
        plagiarism_score
    )
    explanations.extend(notes)

    outlier_value, notes = score_outlier(
        is_outlier
    )
    explanations.extend(notes)

    # ----------------------------------------------------------
    # Final Weighted Probability
    # ----------------------------------------------------------

    probability = calculate_weighted_probability(

        perplexity_value,

        vocabulary_value,

        formality_value,

        consistency_value,

        repetition_value,

        preparedness_value,

        plagiarism_value,

        outlier_value

    )

    # ----------------------------------------------------------
    # Confidence
    # ----------------------------------------------------------

    confidence = abs(probability - 50) * 2

    confidence = round(
        clamp_score(confidence),
        2
    )

    # ----------------------------------------------------------
    # Risk Level
    # ----------------------------------------------------------

    if probability >= 85:

        risk = "Very High"

    elif probability >= 70:

        risk = "High"

    elif probability >= 50:

        risk = "Moderate"

    elif probability >= 30:

        risk = "Low"

    else:

        risk = "Very Low"

    # ----------------------------------------------------------
    # Recommendation
    # ----------------------------------------------------------

    if probability >= 85:

        recommendation = (
            "Very strong indicators of AI-generated "
            "or heavily scripted content."
        )

    elif probability >= 70:

        recommendation = (
            "Response should be manually reviewed."
        )

    elif probability >= 50:

        recommendation = (
            "Mixed linguistic characteristics detected."
        )

    else:

        recommendation = (
            "Response appears predominantly human."
        )

    # ----------------------------------------------------------
    # Remove duplicate explanations
    # ----------------------------------------------------------

    unique_explanations = []

    seen = set()

    for item in explanations:

        if item not in seen:

            unique_explanations.append(item)

            seen.add(item)

    # ----------------------------------------------------------
    # Return
    # ----------------------------------------------------------

    return {

        "ai_probability": probability,

        "confidence": confidence,

        "risk_level": risk,

        "recommendation": recommendation,

        "explanation": unique_explanations

    }