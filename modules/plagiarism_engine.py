"""
==========================================================

Plagiarism Engine

Version 2

Uses Similarity Results to determine
whether an answer appears plagiarized.

==========================================================
"""

from typing import List

from modules.interview_models import (
    SimilarityResult,
    PlagiarismResult,
)


class PlagiarismEngine:
    """
    Determines plagiarism using
    similarity scores.
    """

    def __init__(self):

        self.LOW_THRESHOLD = 0.30

        self.MODERATE_THRESHOLD = 0.60

        self.HIGH_THRESHOLD = 0.80

    def assess(
        self,
        similarity_results: List[SimilarityResult]
    ) -> PlagiarismResult:

        if len(similarity_results) == 0:

            return PlagiarismResult(

                highest_similarity=0.0,

                matched_title="",

                matched_source="",

                matched_content="",

                plagiarism_score=0.0,

                plagiarism_flag=False,

                confidence="None",

                explanation="No reference documents available."

            )

        best_match = similarity_results[0]

        score = best_match.final_score

        plagiarism_score = round(
            score * 100,
            2
        )

        if score >= self.HIGH_THRESHOLD:

            confidence = "Very High"

            plagiarism_flag = True

            explanation = (
                "Similarity exceeded the "
                "high threshold."
            )

        elif score >= self.MODERATE_THRESHOLD:

            confidence = "Moderate"

            plagiarism_flag = False

            explanation = (
                "Moderate similarity detected."
            )

        elif score >= self.LOW_THRESHOLD:

            confidence = "Low"

            plagiarism_flag = False

            explanation = (
                "Minor overlap detected."
            )

        else:

            confidence = "Very Low"

            plagiarism_flag = False

            explanation = (
                "No meaningful plagiarism detected."
            )

        return PlagiarismResult(

            highest_similarity=score,

            matched_title=best_match.title,

            matched_source=best_match.source,

            matched_content=best_match.matched_content,

            plagiarism_score=plagiarism_score,

            plagiarism_flag=plagiarism_flag,

            confidence=confidence,

            explanation=explanation

        )