"""
==============================================================
Outlier Detection Engine

Version 2

Compares an individual interview response against the
candidate's baseline profile.

==============================================================
"""

from modules.interview_models import InterviewResponse

def detect_outlier(
    response: InterviewResponse,
    baseline: dict
):

    if response.metrics is None:
        return None

    metrics = response.metrics
    deviations = {

        "perplexity":
            round(
                abs(
                    metrics["perplexity"] -
                    baseline["perplexity"]["mean"]
                ),
                3
            ),

        "vocabulary":
            round(
                abs(
                    metrics["vocabulary_richness"] -
                    baseline["vocabulary"]["mean"]
                ),
                3
            ),

        "repetition":
            round(
                abs(
                    metrics["repetition_score"] -
                    baseline["repetition"]["mean"]
                ),
                3
            ),

        "formality":
            round(
                abs(
                    metrics["formality_score"] -
                    baseline["formality"]["mean"]
                ),
                3
            ),

        "consistency":
            round(
                abs(
                    metrics["sentence_consistency"] -
                    baseline["consistency"]["mean"]
                ),
                3
            )

    }

    z_scores = {}

    for metric in deviations:

        std = baseline[metric]["std"]

        if std == 0:

            z_scores[metric] = 0

        else:

            z_scores[metric] = round(
                deviations[metric] / std,
                2
            )

    flagged_metrics = []

    for metric, score in z_scores.items():

        if score >= 2:

            flagged_metrics.append(metric)

    overall_score = round(
        sum(z_scores.values()) /
        len(z_scores),
        2
    )
    
    total_metrics = len(deviations)
    
    flag_percentage = round(
        (len(flagged_metrics) / total_metrics) * 100,
        1
    )
    
    return {
        
        "deviations": deviations,
        
        "z_scores": z_scores,
        
        "overall_deviation": overall_score,
        
        "flag_percentage": flag_percentage,
        
        "flagged_metrics": flagged_metrics,
        
        "is_outlier": len(flagged_metrics) > 0
    }