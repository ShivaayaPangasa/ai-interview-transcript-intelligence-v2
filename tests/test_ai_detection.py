from modules.ai_detection_engine import detect_ai_generated_response

result = detect_ai_generated_response(

    perplexity=22,

    vocabulary_richness=0.84,

    sentence_consistency=1.3,

    repetition_score=0.03,

    formality_score=0.06,

    preparedness_score=92,

    plagiarism_score=12,

    is_outlier=False

)

print("=" * 70)
print("AI DETECTION RESULT")
print("=" * 70)

print(f"AI Probability : {result['ai_probability']}")
print(f"Confidence     : {result['confidence']}")
print(f"Risk Level     : {result['risk_level']}")
print(f"Recommendation : {result['recommendation']}")

print()

print("Explanation")

for item in result["explanation"]:

    print("-", item)