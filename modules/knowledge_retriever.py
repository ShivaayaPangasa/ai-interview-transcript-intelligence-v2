"""
==========================================================

Knowledge Retriever

Version 2

Retrieves reference documents for an
interview question.

Pipeline

Interview Question
        │
        ▼
Topic Extractor
        │
        ▼
Wikipedia Summary API
        │
        ▼
If Summary Not Found
        │
        ▼
Wikipedia Search API
        │
        ▼
RetrievedDocument[]

==========================================================
"""

from providers.wikipedia_provider import WikipediaProvider
from modules.topic_extractor import TopicExtractor


class KnowledgeRetriever:
    """
    Retrieves knowledge documents for
    plagiarism detection.
    """

    def __init__(self):

        self.provider = WikipediaProvider()

        self.extractor = TopicExtractor()

    def retrieve(
        self,
        query: str,
        limit: int = 5
    ):
        """
        Retrieves documents relevant
        to the interview question.
        """

        # -----------------------------------
        # Step 1
        # Extract interview topic
        # -----------------------------------

        topic = self.extractor.extract(query)

        # -----------------------------------
        # Step 2
        # Try exact Wikipedia article
        # -----------------------------------

        summary = self.provider.get_summary(topic)

        if summary is not None:

            return [summary]

        # -----------------------------------
        # Step 3
        # Fallback to Wikipedia Search
        # -----------------------------------

        return self.provider.search(

            query=topic,

            limit=limit

        )