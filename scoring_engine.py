MIN_WORDS = 20


def calculate_preparedness_score(

    total_words,
    perplexity,
    vocabulary_richness,
    sentence_consistency,
    repetition_score,
    formality_score

):

    # ==========================
    # SHORT TRANSCRIPT CHECK
    # ==========================

    if total_words < MIN_WORDS:

        return {

            "preparedness_score": None,

            "response_type":
            "Insufficient Transcript Length",

            "confidence": 0,

            "observed_traits": [

                f"Minimum {MIN_WORDS} words required"

            ]
        }

    # ==========================
    # SCORE
    # ==========================

    score = 0

    # PERPLEXITY

    if perplexity < 30:

        score += 30

    elif perplexity < 60:

        score += 20

    else:

        score += 10

    # VOCABULARY

    score += vocabulary_richness * 20

    # SENTENCE CONSISTENCY

    if sentence_consistency < 2:

        score += 15

    elif sentence_consistency < 5:

        score += 10

    else:

        score += 5

    # REPETITION

    score += repetition_score * 20

    # FORMALITY
    
    score += formality_score * 100

    # LIMIT

    score = min(score, 100)

    # ==========================
    # LABEL
    # ==========================


    if score < 45:
        label = "Natural Response"
    
    elif score < 60:
        label = "Prepared Response"
    
    else:
        label = "Highly Structured Response"

    # ==========================
    # TRAITS
    # ==========================

    traits = []

    if vocabulary_richness > 0.80:

        traits.append(
            "Rich Vocabulary"
        )

    if sentence_consistency < 2:

        traits.append(
            "Low Sentence Variation"
        )

    if repetition_score > 0.20:

        traits.append(
            "Repetitive Language"
        )
    
    if formality_score > 0.03:
        
        traits.append(
            "Academic / Formal Language"
    )
        
    if perplexity < 40:

        traits.append(
            "Highly Predictable Text"
        )

    # ==========================
    # CONFIDENCE
    # ==========================

    confidence = min(

        abs(score - 50) * 2,

        100

    )

    # ==========================
    # RETURN
    # ==========================

    return {

        "preparedness_score": round(
            score,
            2
        ),

        "response_type": label,

        "confidence": round(
            confidence,
            2
        ),

        "observed_traits": traits
    }