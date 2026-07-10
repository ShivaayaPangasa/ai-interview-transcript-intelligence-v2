from modules.authenticity_engine import AuthenticityEngine

engine = AuthenticityEngine()

result = engine.assess(

    preparedness_score=82,

    plagiarism_score=15,

    outlier_flag=False,

    ai_probability=12

)

print("=" * 70)
print("AUTHENTICITY RESULT")
print("=" * 70)

print(f"Preparedness     : {result.preparedness_score}")
print(f"Plagiarism       : {result.plagiarism_score}")
print(f"Outlier Score    : {result.outlier_score}")
print(f"AI Probability   : {result.ai_probability}")

print()

print(f"Authenticity     : {result.authenticity_score}")
print(f"Risk Level       : {result.risk_level}")
print(f"Recommendation   : {result.recommendation}")

print()

print("Explanation")

print(result.explanation)