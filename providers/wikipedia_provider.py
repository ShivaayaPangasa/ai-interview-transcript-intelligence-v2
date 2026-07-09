"""
==========================================================

Wikipedia Provider

Version 2

Retrieves reference documents
from Wikipedia.

==========================================================
"""

import html
import re
import requests

from modules.interview_models import RetrievedDocument


class WikipediaProvider:

    BASE_URL = "https://en.wikipedia.org/w/api.php"

    SUMMARY_URL = (
        "https://en.wikipedia.org/api/rest_v1/page/summary/"
    )

    HEADERS = {

        "User-Agent": (
            "AIInterviewTranscriptIntelligence/2.0"
        )

    }

    def search(
        self,
        query: str,
        limit: int = 5
    ):

        parameters = {

            "action": "query",

            "list": "search",

            "srsearch": query,

            "format": "json",

            "srlimit": limit

        }

        response = requests.get(

            self.BASE_URL,

            params=parameters,

            headers=self.HEADERS,

            timeout=10

        )

        data = response.json()

        search_results = data.get(
            "query",
            {}
        ).get(
            "search",
            []
        )

        documents = []

        for article in search_results:

            title = article.get("title", "")

            summary_response = requests.get(

                self.SUMMARY_URL + title,

                headers=self.HEADERS,

                timeout=10

            )

            if summary_response.status_code != 200:

                continue

            summary = summary_response.json()

            content = summary.get("extract", "")

            content = re.sub(
                r"<.*?>",
                "",
                content
            )

            content = html.unescape(content)

            document = RetrievedDocument(

                title=title,

                url=summary.get(

                    "content_urls",

                    {}

                ).get(

                    "desktop",

                    {}

                ).get(

                    "page",

                    ""

                ),

                content=content,

                source="Wikipedia"

            )

            documents.append(document)

        return documents
    
    def get_summary(
    self,
    topic: str
    ):
        
        """
        Retrieves the Wikipedia summary
        for an exact topic.
        """
        
        url = (
            "https://en.wikipedia.org/api/rest_v1/"
            f"page/summary/{topic.replace(' ', '_')}"
        )

        headers = {
            "User-Agent":
            "InterviewIntelligence/1.0"
        }

        response = requests.get(
            url,
            headers=headers,
            timeout=10
        )

        if response.status_code != 200:
            
            return None

        data = response.json()

        if "extract" not in data:
            
            return None

        return RetrievedDocument(
            
            title=data["title"],

            source="Wikipedia",

            url=data["content_urls"]["desktop"]["page"],

            content=data["extract"]

        )