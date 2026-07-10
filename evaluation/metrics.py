import pandas as pd

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report
)

# ----------------------------------------
# Load Results
# ----------------------------------------

df = pd.read_csv("evaluation/results.csv")

y_true = df["ground_truth"]
y_pred = df["prediction"]

# ----------------------------------------
# Calculate Metrics
# ----------------------------------------

accuracy = accuracy_score(y_true, y_pred)

precision = precision_score(
    y_true,
    y_pred,
    average="weighted",
    zero_division=0
)

recall = recall_score(
    y_true,
    y_pred,
    average="weighted",
    zero_division=0
)

f1 = f1_score(
    y_true,
    y_pred,
    average="weighted",
    zero_division=0
)

report = classification_report(
    y_true,
    y_pred,
    zero_division=0
)

# ----------------------------------------
# Display
# ----------------------------------------

print("\n==============================")
print("MODEL EVALUATION")
print("==============================")

print(f"Accuracy : {accuracy:.3f}")
print(f"Precision: {precision:.3f}")
print(f"Recall   : {recall:.3f}")
print(f"F1 Score : {f1:.3f}")

print("\nClassification Report\n")
print(report)

# ----------------------------------------
# Save Report
# ----------------------------------------

with open(
    "evaluation/evaluation_report.txt",
    "w",
    encoding="utf-8"
) as file:

    file.write("==============================\n")
    file.write("MODEL EVALUATION REPORT\n")
    file.write("==============================\n\n")

    file.write(f"Total Samples : {len(df)}\n\n")

    file.write(f"Accuracy  : {accuracy:.4f}\n")
    file.write(f"Precision : {precision:.4f}\n")
    file.write(f"Recall    : {recall:.4f}\n")
    file.write(f"F1 Score  : {f1:.4f}\n\n")

    file.write("Classification Report\n")
    file.write("---------------------\n\n")

    file.write(report)

print("\nEvaluation report saved to:")
print("evaluation/evaluation_report.txt")