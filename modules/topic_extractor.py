"""
==========================================================

Topic Extractor

Version 2

Extracts the main interview topic from
an interview question.

This module is intentionally rule-based
to avoid LLM hallucinations.

==========================================================
"""

import re


class TopicExtractor:

    def extract(
        self,
        question: str
    ) -> str:
        """
        Extracts the likely topic from an
        interview question.
        """

        question = question.lower()

        prefixes = [

            "what is",

            "what are",

            "explain",

            "describe",

            "define",

            "tell me about",

            "can you explain",

            "please explain",

            "how does",

            "difference between"

        ]

        for prefix in prefixes:

            if question.startswith(prefix):

                question = question.replace(
                    prefix,
                    "",
                    1
                )

        question = re.sub(
            r"[?.!,]",
            "",
            question
        )

        question = " ".join(
            question.split()
        )

        return question.title()