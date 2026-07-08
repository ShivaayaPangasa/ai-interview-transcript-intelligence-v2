"""
==========================================================

Knowledge Retriever

Version 2

Coordinates retrieval of reference documents.

The retriever itself does NOT know
whether documents come from:

• Wikipedia
• Google
• Company Knowledge Base

It only talks to a provider.

==========================================================
"""

from providers.wikipedia_provider import WikipediaProvider


class KnowledgeRetriever:
    """
    Coordinates retrieval
    of reference documents.
    """

    def __init__(self):

        self.provider = WikipediaProvider()

    def retrieve(
        self,
        query: str,
        limit: int = 5
    ):

        """
        Retrieve reference documents
        related to an interview query.
        """

        documents = self.provider.search(

            query=query,

            limit=limit

        )

        return documents