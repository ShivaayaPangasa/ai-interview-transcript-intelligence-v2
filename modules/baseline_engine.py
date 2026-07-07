"""
==========================================================
Candidate Baseline Engine

Version 2

Generates a candidate-specific linguistic baseline
using all interview responses.

This baseline is later used for:

• Outlier Detection
• AI Flagging
• Adaptive Thresholds
• Interview Assessment

==========================================================
"""

from modules.interview_models import InterviewSession


def generate_candidate_baseline(
    session: InterviewSession
):
    """
    Computes average linguistic metrics
    across an interview session.
    """

    total_perplexity = 0

    total_vocabulary = 0

    total_repetition = 0

    total_formality = 0

    total_consistency = 0

    valid_responses = 0

    for response in session.responses:

        if response.metrics is None:

            continue

        total_perplexity += response.metrics["perplexity"]

        total_vocabulary += response.metrics["vocabulary_richness"]

        total_repetition += response.metrics["repetition_score"]

        total_formality += response.metrics["formality_score"]

        total_consistency += response.metrics["sentence_consistency"]

        valid_responses += 1

    if valid_responses == 0:

        return None

    baseline = {

        "average_perplexity":
            round(
                total_perplexity / valid_responses,
                2
            ),

        "average_vocabulary":
            round(
                total_vocabulary / valid_responses,
                3
            ),

        "average_repetition":
            round(
                total_repetition / valid_responses,
                3
            ),

        "average_formality":
            round(
                total_formality / valid_responses,
                3
            ),

        "average_consistency":
            round(
                total_consistency / valid_responses,
                3
            ),

        "responses_used":
            valid_responses
    }

    return baseline