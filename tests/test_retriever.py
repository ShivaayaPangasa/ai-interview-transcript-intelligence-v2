from modules.knowledge_retriever import KnowledgeRetriever


retriever = KnowledgeRetriever()

documents = retriever.retrieve(

    query="Explain Overfitting",

    limit=3

)

print("=" * 60)
print("KNOWLEDGE RETRIEVER")
print("=" * 60)

for document in documents:

    print(f"Title    : {document.title}")

    print(f"Source   : {document.source}")

    print(f"URL      : {document.url}")

    print(f"Snippet  : {document.snippet}")

    print("-" * 60)