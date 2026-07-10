"""
==============================================================
Interview Data Models

Version 2

These classes define the structure of an interview session.

No AI logic is implemented here.

They simply act as containers that every engine
(Baseline, Similarity, AI Flag, Reporting)
will use throughout the pipeline.

==============================================================
"""

# ==============================================================
# INDIVIDUAL INTERVIEW RESPONSE
# ==============================================================

from dataclasses import dataclass, field
from typing import List, Optional
@dataclass
class RetrievedDocument:
    """
    Represents one retrieved
    reference document.
    """

    title: str

    url: str

    content: str

    source: str

    similarity: Optional[float] = None

@dataclass
class SimilarityResult:
    """
    Represents similarity between a
    candidate answer and one
    retrieved reference document.
    """

    title: str

    source: str

    matched_content: str

    tfidf_score: float

    ngram_score: float

    jaccard_score: float

    final_score: float
    
@dataclass
class PlagiarismResult:
    """
    Represents the plagiarism assessment
    for one interview response.
    """

    highest_similarity: float

    matched_title: str

    matched_source: str

    matched_content: str

    plagiarism_score: float

    plagiarism_flag: bool

    confidence: str

    explanation: str
    
@dataclass
class InterviewResponse:
    """
    Represents one interview question and answer.
    """

    question: str

    answer: str

    metrics: Optional[dict] = None

    preparedness: Optional[dict] = None

    similarity: Optional[dict] = None

    baseline_deviation: Optional[dict] = None

    ai_flag: Optional[dict] = None
    
    authenticity: Optional[dict] = None
    
    retrieved_documents: list = field(default_factory=list)

# ==============================================================
# COMPLETE INTERVIEW SESSION
# ==============================================================

@dataclass
class InterviewSession:
    """
    Represents an entire interview consisting
    of multiple question-answer pairs.
    """

    candidate_name: str

    interview_id: str

    responses: List[InterviewResponse] = field(default_factory=list)

    baseline: Optional[dict] = None

    summary: Optional[dict] = None

    overall_assessment: Optional[dict] = None

@dataclass
class AuthenticityResult:
    """
    Final authenticity assessment for
    one interview response.
    """

    preparedness_score: float

    plagiarism_score: float

    outlier_score: float

    ai_probability: float

    authenticity_score: float

    risk_level: str

    recommendation: str

    explanation: str