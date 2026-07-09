from modules.knowledge_retriever import KnowledgeRetriever
from modules.similarity_engine import SimilarityEngine
from modules.plagiarism_engine import PlagiarismEngine


candidate_answer = """
Overfitting occurs when a machine learning
model memorizes the training data instead
of learning general patterns.
"""


retriever = KnowledgeRetriever()

documents = retriever.retrieve(
    "Overfitting"
)

similarity_engine = SimilarityEngine()

similarity_results = similarity_engine.compare(

    candidate_answer,

    documents

)

plagiarism_engine = PlagiarismEngine()

result = plagiarism_engine.assess(

    similarity_results

)

print("=" * 70)

print("PLAGIARISM RESULT")

print("=" * 70)

print(f"Highest Similarity : {result.highest_similarity}")

print(f"Plagiarism Score   : {result.plagiarism_score}")

print(f"Matched Title      : {result.matched_title}")

print(f"Matched Source     : {result.matched_source}")

print(f"Confidence         : {result.confidence}")

print(f"Flag               : {result.plagiarism_flag}")

print()

print("Explanation")

print(result.explanation)

print()

print("Matched Content")

print(result.matched_content[:300])