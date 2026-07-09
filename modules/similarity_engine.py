"""
==========================================================

Similarity Engine

Version 2

Computes similarity between a candidate's
response and retrieved reference documents.

Algorithms Implemented

• TF-IDF + Cosine Similarity
• N-Gram Similarity
• Jaccard Similarity

==========================================================
"""

import re
from typing import List

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from modules.interview_models import (
    RetrievedDocument,
    SimilarityResult,
)


class SimilarityEngine:
    """
    Computes multiple similarity scores
    between a candidate answer and
    retrieved reference documents.
    """

    def __init__(self):
        """
        Weight assigned to each similarity metric.

        Final Score =
            50% TF-IDF
            30% N-Gram
            20% Jaccard
        """
        
        self.TFIDF_WEIGHT = 0.60
        self.NGRAM_WEIGHT = 0.20
        self.JACCARD_WEIGHT = 0.20

    # ======================================================
    # Text Preprocessing
    # ======================================================

    def preprocess_text(
        self,
        text: str
    ) -> str:
        """
        Basic text preprocessing.

        - Convert to lowercase
        - Remove punctuation
        - Remove extra whitespace
        """

        text = text.lower()

        text = re.sub(
            r"[^a-z0-9\s]",
            "",
            text
        )

        text = re.sub(
            r"\s+",
            " ",
            text
        ).strip()

        return text

    # ======================================================
    # TF-IDF Similarity
    # ======================================================

    def calculate_tfidf_similarity(
        self,
        answer: str,
        document: str
    ) -> float:
        """
        Computes TF-IDF Cosine Similarity.
        """

        vectorizer = TfidfVectorizer()

        matrix = vectorizer.fit_transform(
            [answer, document]
        )

        similarity = cosine_similarity(
            matrix[0:1],
            matrix[1:2]
        )[0][0]

        return round(float(similarity), 3)

    # ======================================================
    # N-Gram Similarity
    # ======================================================

    def calculate_ngram_similarity(
        self,
        answer: str,
        document: str,
        n: int = 2
    ) -> float:
        """
        Computes N-Gram similarity using
        Jaccard overlap over n-grams.
        """

        answer_words = answer.split()
        document_words = document.split()

        answer_ngrams = set(
            zip(*[
                answer_words[i:]
                for i in range(n)
            ])
        )

        document_ngrams = set(
            zip(*[
                document_words[i:]
                for i in range(n)
            ])
        )

        if not answer_ngrams or not document_ngrams:
            return 0.0

        intersection = len(
            answer_ngrams.intersection(
                document_ngrams
            )
        )

        union = len(
            answer_ngrams.union(
                document_ngrams
            )
        )

        return round(
            intersection / union,
            3
        )

    # ======================================================
    # Jaccard Similarity
    # ======================================================

    def calculate_jaccard_similarity(
        self,
        answer: str,
        document: str
    ) -> float:
        """
        Computes word-level
        Jaccard similarity.
        """

        answer_words = set(
            answer.split()
        )

        document_words = set(
            document.split()
        )

        intersection = len(
            answer_words.intersection(
                document_words
            )
        )

        union = len(
            answer_words.union(
                document_words
            )
        )

        if union == 0:
            return 0.0

        return round(
            intersection / union,
            3
        )

    # ======================================================
    # Final Weighted Score
    # ======================================================

    def calculate_final_score(
        self,
        tfidf_score: float,
        ngram_score: float,
        jaccard_score: float
    ) -> float:
        """
        Computes the weighted
        final similarity score.
        """

        score = (

            tfidf_score * self.TFIDF_WEIGHT +

            ngram_score * self.NGRAM_WEIGHT +

            jaccard_score * self.JACCARD_WEIGHT

        )

        return round(
            score,
            3
        )

    # ======================================================
    # Compare Candidate Answer
    # ======================================================

    def compare(
        self,
        candidate_answer: str,
        documents: List[RetrievedDocument]
    ) -> List[SimilarityResult]:
        """
        Compare a candidate answer against all
        retrieved reference documents.
        """

        results = []

        # Preprocess candidate answer
        candidate_answer = self.preprocess_text(
            candidate_answer
        )

        for document in documents:

            # Preprocess document content
            document_content = self.preprocess_text(
                document.content
            )

            # Calculate individual similarity scores
            tfidf_score = self.calculate_tfidf_similarity(
                candidate_answer,
                document_content
            )

            ngram_score = self.calculate_ngram_similarity(
                candidate_answer,
                document_content
            )

            jaccard_score = self.calculate_jaccard_similarity(
                candidate_answer,
                document_content
            )

            # Calculate weighted score
            final_score = self.calculate_final_score(
                tfidf_score,
                ngram_score,
                jaccard_score
            )

            # Store result
            similarity = SimilarityResult(

                title=document.title,

                source=document.source,

                matched_content=document.content,

                tfidf_score=tfidf_score,

                ngram_score=ngram_score,

                jaccard_score=jaccard_score,

                final_score=final_score

            )

            results.append(similarity)

        # Highest similarity first
        results.sort(

            key=lambda result: result.final_score,

            reverse=True

        )

        return results