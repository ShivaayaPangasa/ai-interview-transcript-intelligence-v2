import pandas as pd

import matplotlib.pyplot as plt

from sklearn.metrics import ConfusionMatrixDisplay

from sklearn.metrics import confusion_matrix


df = pd.read_csv(

    "evaluation/results.csv"

)

labels = [

    "Genuine",

    "AI",

    "Wikipedia"

]

cm = confusion_matrix(

    df["ground_truth"],

    df["prediction"],

    labels=labels

)

disp = ConfusionMatrixDisplay(

    confusion_matrix=cm,

    display_labels=labels

)

disp.plot(

    cmap="Blues"

)

plt.title(

    "Transcript Intelligence Confusion Matrix"

)

plt.tight_layout()

plt.savefig(

    "evaluation/confusion_matrix.png",

    dpi=300

)

plt.show()