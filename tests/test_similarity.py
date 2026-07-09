"""
==========================================================

Similarity Engine Test

==========================================================
"""

from modules.knowledge_retriever import KnowledgeRetriever
from modules.similarity_engine import SimilarityEngine


candidate_answer = """
Overfitting occurs when a machine learning
model memorizes the training data instead
of learning general patterns.
"""


print("=" * 70)
print("Retrieving Reference Documents...")
print("=" * 70)

retriever = KnowledgeRetriever()

documents = retriever.retrieve(

    query="Explain Overfitting",

    limit=5

)

print(f"Retrieved {len(documents)} documents.")

print()

engine = SimilarityEngine()

results = engine.compare(

    candidate_answer,

    documents

)

print("=" * 70)
print("SIMILARITY RESULTS")
print("=" * 70)

for result in results:

    print(f"Title           : {result.title}")

    print(f"Source          : {result.source}")

    print(f"TF-IDF Score    : {result.tfidf_score}")

    print(f"N-Gram Score    : {result.ngram_score}")

    print(f"Jaccard Score   : {result.jaccard_score}")

    print(f"Final Score     : {result.final_score}")

    print()

    print("Matched Content")

    print(result.matched_content[:250])

    print()

    print("-" * 70)