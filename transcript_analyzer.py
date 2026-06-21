import re
import numpy as np
from collections import Counter


def analyze_transcript(transcript):

    # ==========================
    # WORD ANALYSIS
    # ==========================

    words = re.findall(
        r"\b\w+\b",
        transcript.lower()
    )

    total_words = len(words)

    unique_words = len(set(words))

    vocabulary_richness = (
        unique_words / total_words
    ) if total_words > 0 else 0

    # ==========================
    # SENTENCE ANALYSIS
    # ==========================

    sentences = re.split(
        r"[.!?]+",
        transcript
    )

    sentences = [
        s.strip()
        for s in sentences
        if s.strip()
    ]

    sentence_lengths = []

    for sentence in sentences:

        sentence_words = re.findall(
            r"\b\w+\b",
            sentence
        )

        sentence_lengths.append(
            len(sentence_words)
        )

    if len(sentence_lengths) > 1:

        sentence_consistency = float(
            np.std(sentence_lengths)
        )

    else:

        sentence_consistency = 0

    # ==========================
    # REPETITION SCORE
    # ==========================

    word_counts = Counter(words)

    most_common_count = 0

    if total_words > 0:

        most_common_count = (
            word_counts.most_common(1)[0][1]
        )

    repetition_score = (
        most_common_count /
        total_words
    ) if total_words > 0 else 0

    # ==========================
    # FORMALITY SCORE
    # ==========================

    formal_words = {

        "therefore",
        "furthermore",
        "moreover",
        "consequently",
        "hence",
        "thus",
        "additionally",
        "accordingly",
        "indeed",
        "notwithstanding",
        "firstly",
        "secondly",
        "thirdly",
        "finally",
        "in_conclusion",
        "in_summary",
        "conclusion",
        "summary"
    }

    formal_count = sum(
        1
        for word in words
        if word in formal_words
    )

    formality_score = (
        formal_count /
        total_words
    ) if total_words > 0 else 0

    # ==========================
    # RETURN
    # ==========================

    return {

        "total_words": total_words,

        "unique_words": unique_words,

        "vocabulary_richness": round(
            vocabulary_richness,
            3
        ),

        "sentence_consistency": round(
            sentence_consistency,
            3
        ),

        "repetition_score": round(
            repetition_score,
            3
        ),

        "formality_score": round(
            formality_score,
            3
        )
    }