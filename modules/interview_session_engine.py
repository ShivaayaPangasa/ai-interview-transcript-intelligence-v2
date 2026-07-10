"""
==============================================================

Interview Session Engine

Version 2

This module manages an entire interview session.

Responsibilities

• Create Interview Session
• Store Interview Responses
• Generate Final Interview Summary
• Save Interview Results

No NLP logic is implemented here.

This engine only orchestrates and stores the
outputs produced by other engines.

==============================================================
"""

import json
import os
from datetime import datetime
from typing import Optional

from modules.interview_models import (
    InterviewSession,
    InterviewResponse
)


# ==============================================================
# CREATE INTERVIEW SESSION
# ==============================================================

def create_session(

    candidate_name: str,
    interview_id: str

) -> InterviewSession:
    """
    Creates a new interview session.
    """

    session = InterviewSession(

        candidate_name=candidate_name,

        interview_id=interview_id,

        responses=[],

        baseline=None,

        summary=None,

        overall_assessment=None

    )

    return session


# ==============================================================
# ADD RESPONSE
# ==============================================================

def add_response(

    session: InterviewSession,

    question: str,

    answer: str,

    metrics: Optional[dict] = None,

    preparedness: Optional[dict] = None,

    similarity: Optional[dict] = None,

    baseline_deviation: Optional[dict] = None,

    ai_flag: Optional[dict] = None,

    authenticity: Optional[dict] = None,

    retrieved_documents: Optional[list] = None

):
    """
    Adds one analysed interview response
    to the interview session.
    """

    response = InterviewResponse(

        question=question,

        answer=answer,

        metrics=metrics,

        preparedness=preparedness,

        similarity=similarity,

        baseline_deviation=baseline_deviation,

        ai_flag=ai_flag,
        
        authenticity=authenticity,

        retrieved_documents=(
            retrieved_documents
            if retrieved_documents
            else []
        )

    )

    # Store authenticity separately until
    # the InterviewResponse dataclass is updated.

    session.responses.append(response)


# ==============================================================
# SAFE AVERAGE
# ==============================================================

def safe_average(values):
    """
    Returns the average of all valid numbers.
    """

    valid = [

        value

        for value in values

        if value is not None

    ]

    if len(valid) == 0:

        return 0

    return round(

        sum(valid) /

        len(valid),

        2

    )


# ==============================================================
# COUNT FLAGGED RESPONSES
# ==============================================================

def count_flagged_questions(

    session: InterviewSession

):

    count = 0

    for response in session.responses:

        if response.ai_flag is None:

            continue

        probability = response.ai_flag.get(

            "ai_probability",

            0

        )

        if probability >= 70:

            count += 1

    return count

# ==============================================================
# GENERATE INTERVIEW SUMMARY
# ==============================================================

def generate_summary(
    session: InterviewSession
):
    """
    Computes interview-level statistics
    across all recorded responses.
    """

    preparedness_scores = []

    plagiarism_scores = []

    ai_scores = []

    authenticity_scores = []

    for response in session.responses:

        # -----------------------------
        # Preparedness
        # -----------------------------

        if response.preparedness is not None:

            preparedness_scores.append(

                response.preparedness.get(

                    "preparedness_score"

                )

            )

        # -----------------------------
        # Similarity / Plagiarism
        # -----------------------------

        if response.similarity is not None:

            plagiarism_scores.append(

                response.similarity.get(

                    "plagiarism_score"

                )

            )

        # -----------------------------
        # AI Detection
        # -----------------------------

        if response.ai_flag is not None:

            ai_scores.append(

                response.ai_flag.get(

                    "ai_probability"

                )

            )

        # -----------------------------
        # Authenticity
        # -----------------------------
        
        if response.authenticity is not None:
            
                authenticity_scores.append(

                    response.authenticity.get(

                        "authenticity_score"

                    )

                )

    average_preparedness = safe_average(

        preparedness_scores

    )

    average_plagiarism = safe_average(

        plagiarism_scores

    )

    average_ai = safe_average(

        ai_scores

    )

    average_authenticity = safe_average(

        authenticity_scores

    )

    flagged_questions = count_flagged_questions(

        session

    )

    # -------------------------------------------------
    # Overall Recommendation
    # -------------------------------------------------

    if average_authenticity >= 85:

        recommendation = "Likely Genuine"

    elif average_authenticity >= 70:

        recommendation = "Probably Genuine"

    elif average_authenticity >= 50:

        recommendation = "Needs Manual Review"

    elif average_authenticity >= 30:

        recommendation = "Suspicious Interview"

    else:

        recommendation = "Likely AI Generated / Copied"

    summary = {

        "candidate_name":

            session.candidate_name,

        "interview_id":

            session.interview_id,

        "total_questions":

            len(session.responses),

        "average_preparedness":

            average_preparedness,

        "average_plagiarism":

            average_plagiarism,

        "average_ai_probability":

            average_ai,

        "overall_authenticity":

            average_authenticity,

        "flagged_questions":

            flagged_questions,

        "recommendation":

            recommendation,

        "generated_at":

            datetime.now().strftime(

                "%Y-%m-%d %H:%M:%S"

            )

    }

    session.summary = summary

    return summary


# ==============================================================
# SAVE SESSION
# ==============================================================

def save_session(
    session: InterviewSession,
    folder="interviews"
):
    """
    Saves the completed interview session
    as a JSON file.
    """

    os.makedirs(

        folder,

        exist_ok=True

    )

    if session.summary is None:

        generate_summary(

            session

        )

    responses = []

    for response in session.responses:

        responses.append({

            "question":

                response.question,

            "answer":

                response.answer,

            "metrics":

                response.metrics,

            "preparedness":

                response.preparedness,

            "similarity":

                response.similarity,

            "baseline_deviation":

                response.baseline_deviation,

            "ai_flag":

                response.ai_flag,
            
            "authenticity":
                
                response.authenticity,

            "retrieved_documents":[

                vars(document)

                for document

                in response.retrieved_documents

            ]

        })

    interview = {

        "candidate_name":

            session.candidate_name,

        "interview_id":

            session.interview_id,

        "baseline":

            session.baseline,

        "summary":

            session.summary,

        "responses":

            responses

    }

    filename = os.path.join(

        folder,

        f"{session.interview_id}.json"

    )

    with open(

        filename,

        "w",

        encoding="utf-8"

    ) as file:

        json.dump(

            interview,

            file,

            indent=4,

            ensure_ascii=False

        )

    return filename