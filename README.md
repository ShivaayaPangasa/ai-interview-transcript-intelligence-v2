# AI Interview Transcript Intelligence

An AI-powered interview transcript intelligence system for real-time analysis of spoken interview responses.

## Features

- Speech-to-Text using Whisper
- Transcript Linguistic Analysis
- Perplexity Estimation
- Candidate Preparedness Scoring
- Knowledge Retrieval
- Semantic Similarity Search
- Plagiarism Detection
- Candidate Baseline Modeling
- Outlier Detection
- AI-generated Response Detection
- Authenticity Assessment
- Interview Session Tracking
- JSON Interview Export
- Evaluation Framework
- Confusion Matrix
- Accuracy / Precision / Recall / F1 Metrics

---

## Technology Stack

- Python
- Streamlit
- Whisper
- SentenceTransformers
- HuggingFace Transformers
- Scikit-learn
- Pandas
- NumPy
- Matplotlib

---

## Project Workflow

Candidate Speech

↓

Whisper Speech Recognition

↓

Transcript Analysis

↓

Perplexity Estimation

↓

Knowledge Retrieval

↓

Semantic Similarity

↓

Plagiarism Detection

↓

Preparedness Analysis

↓

Candidate Baseline

↓

Outlier Detection

↓

AI Detection

↓

Authenticity Assessment

↓

Interview Summary

↓

Evaluation Metrics

---

## Evaluation

The system supports manual ground-truth labels:

- Genuine
- AI
- Wikipedia

Each interview is automatically logged into:

```
evaluation/results.csv
```

Evaluation includes:

- Accuracy
- Precision
- Recall
- F1-score
- Confusion Matrix

---

## Repository Structure

```
app.py
modules/
evaluation/
interviews/
tests/
```

---

## Future Improvements

- LLM-based semantic reasoning
- Eye gaze tracking
- Voice emotion analysis
- Prosody analysis
- Live dashboard
- Multi-modal interview intelligence

---

Developed as part of the AI Engineering Internship at Einstellen.ai.
