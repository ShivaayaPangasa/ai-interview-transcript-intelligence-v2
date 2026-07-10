import csv
import os


RESULTS_FILE = "evaluation/results.csv"


def save_evaluation(

    candidate,

    question,

    ground_truth,

    prediction,

    ai_probability,

    plagiarism_score,

    authenticity_score

):

    file_exists = os.path.exists(RESULTS_FILE)

    with open(

        RESULTS_FILE,

        "a",

        newline="",

        encoding="utf-8"

    ) as file:

        writer = csv.writer(file)

        if not file_exists or os.path.getsize(RESULTS_FILE) == 0:

            writer.writerow([

                "candidate",

                "question",

                "ground_truth",

                "prediction",

                "ai_probability",

                "plagiarism_score",

                "authenticity_score"

            ])

        writer.writerow([

            candidate,

            question,

            ground_truth,

            prediction,

            round(ai_probability, 2),

            round(plagiarism_score, 2),

            round(authenticity_score, 2)

        ])