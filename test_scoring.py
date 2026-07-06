from preparedness_engine import (
    calculate_preparedness_score
)

result = calculate_preparedness_score(

    perplexity=26.88,

    vocabulary_richness=0.90,

    sentence_consistency=1.22,

    repetition_score=0.15,

    formality_score=0.15
)

print(result)