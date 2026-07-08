from providers.wikipedia_provider import WikipediaProvider


provider = WikipediaProvider()

documents = provider.search(

    query="What is Overfitting?",

    limit=3

)

print("=" * 60)
print("RETRIEVED DOCUMENTS")
print("=" * 60)

for document in documents:

    print(f"Title      : {document.title}")

    print(f"URL        : {document.url}")

    print(f"Source     : {document.source}")
    
    print("=" * 70)

    print(f"TITLE   : {document.title}")

    print()

    print(f"SOURCE  : {document.source}")

    print()

    print(f"URL     : {document.url}")

    print()

    print("CONTENT")

    print(document.content)

    print()

    print("=" * 70)
