"""
==============================================================

Outlier Detection Engine

Version 2

Detects whether a response significantly deviates
from the candidate's baseline profile.

Input

Metrics Dictionary

+

Candidate Baseline

Output

Deviation Statistics

==============================================================
"""


def detect_outlier(
    metrics: dict,
    baseline: dict
):
    """
    Compares one response against the
    candidate's linguistic baseline.
    """

    # ---------------------------------------------------------
    # Safety Checks
    # ---------------------------------------------------------

    if metrics is None:

        return None

    if baseline is None:

        return None

    # ---------------------------------------------------------
    # Absolute Deviations
    # ---------------------------------------------------------

    deviations = {

        "perplexity":

            round(

                abs(

                    metrics["perplexity"]

                    -

                    baseline["perplexity"]["mean"]

                ),

                3

            ),

        "vocabulary":

            round(

                abs(

                    metrics["vocabulary_richness"]

                    -

                    baseline["vocabulary"]["mean"]

                ),

                3

            ),

        "repetition":

            round(

                abs(

                    metrics["repetition_score"]

                    -

                    baseline["repetition"]["mean"]

                ),

                3

            ),

        "formality":

            round(

                abs(

                    metrics["formality_score"]

                    -

                    baseline["formality"]["mean"]

                ),

                3

            ),

        "consistency":

            round(

                abs(

                    metrics["sentence_consistency"]

                    -

                    baseline["consistency"]["mean"]

                ),

                3

            )

    }

    # ---------------------------------------------------------
    # Z Scores
    # ---------------------------------------------------------

    z_scores = {}

    for metric in deviations:

        std = baseline[metric]["std"]

        if std == 0:

            z_scores[metric] = 0

        else:

            z_scores[metric] = round(

                deviations[metric] /

                std,

                2

            )

    # ---------------------------------------------------------
    # Flag Metrics
    # ---------------------------------------------------------

    flagged_metrics = []

    for metric, score in z_scores.items():

        if score >= 2:

            flagged_metrics.append(

                metric

            )

    # ---------------------------------------------------------
    # Overall Deviation
    # ---------------------------------------------------------

    overall_deviation = round(

        sum(

            z_scores.values()

        )

        /

        len(z_scores),

        2

    )

    flag_percentage = round(

        (

            len(flagged_metrics)

            /

            len(deviations)

        )

        *

        100,

        1

    )

    # ---------------------------------------------------------
    # Return
    # ---------------------------------------------------------

    return {

        "deviations":

            deviations,

        "z_scores":

            z_scores,

        "overall_deviation":

            overall_deviation,

        "flag_percentage":

            flag_percentage,

        "flagged_metrics":

            flagged_metrics,

        "is_outlier":

            len(flagged_metrics) > 0

    }