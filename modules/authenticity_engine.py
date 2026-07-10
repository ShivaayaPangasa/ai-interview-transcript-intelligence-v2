"""
==========================================================

Authenticity Engine

Version 2

Combines all individual engine outputs into
one explainable authenticity assessment.

==========================================================
"""

from modules.interview_models import AuthenticityResult


class AuthenticityEngine:
    """
    Produces the final authenticity score
    for one interview response.
    """

    def __init__(self):

        self.preparedness_weight = 0.30

        self.outlier_weight = 0.25

        self.plagiarism_weight = 0.35

        self.ai_weight = 0.10

    def assess(
        self,
        preparedness_score: float,
        plagiarism_score: float,
        outlier_flag: bool,
        ai_probability: float = 0.0
    ) -> AuthenticityResult:

        # -----------------------------
        # Outlier score
        # -----------------------------

        outlier_score = 100 if outlier_flag else 0

        # -----------------------------
        # Authenticity Calculation
        # -----------------------------

        authenticity = (

            preparedness_score * self.preparedness_weight

            +

            (100 - plagiarism_score) * self.plagiarism_weight

            +

            (100 - outlier_score) * self.outlier_weight

            +

            (100 - ai_probability) * self.ai_weight

        )

        authenticity = round(authenticity, 2)

        # -----------------------------
        # Risk Level
        # -----------------------------

        if authenticity >= 85:

            risk = "Very Low"

            recommendation = "Likely Genuine"

        elif authenticity >= 70:

            risk = "Low"

            recommendation = "Probably Genuine"

        elif authenticity >= 50:

            risk = "Moderate"

            recommendation = "Needs Manual Review"

        elif authenticity >= 30:

            risk = "High"

            recommendation = "Suspicious"

        else:

            risk = "Very High"

            recommendation = "Likely AI / Copied"

        # -----------------------------
        # Explanation
        # -----------------------------

        explanation = (

            f"Preparedness: {preparedness_score:.1f}, "

            f"Plagiarism: {plagiarism_score:.1f}, "

            f"Outlier: {'Yes' if outlier_flag else 'No'}, "

            f"AI Probability: {ai_probability:.1f}"

        )

        return AuthenticityResult(

            preparedness_score=preparedness_score,

            plagiarism_score=plagiarism_score,

            outlier_score=outlier_score,

            ai_probability=ai_probability,

            authenticity_score=authenticity,

            risk_level=risk,

            recommendation=recommendation,

            explanation=explanation

        )