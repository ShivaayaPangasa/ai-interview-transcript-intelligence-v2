# Interview Transcript Intelligence System

Real-time linguistic analysis of spoken interview responses using Whisper Speech Recognition, GPT-2 Perplexity Analysis, and NLP-based transcript intelligence.

---

## Overview

Interview Transcript Intelligence System is an end-to-end NLP application designed to analyze spoken interview responses and extract meaningful linguistic characteristics from candidate speech.

The system records audio responses, converts speech to text using OpenAI Whisper, computes multiple linguistic metrics, and generates a Preparedness Score based on transcript structure and language patterns.

Rather than attempting to claim whether a response was AI-generated, the system focuses on observable linguistic characteristics such as vocabulary diversity, sentence structure, repetition, formality, and text predictability.

---

## Features

### Speech Processing

* Real-time microphone recording
* Start / Stop recording controls
* OpenAI Whisper speech-to-text transcription
* Local inference pipeline

### Transcript Intelligence

* Vocabulary Richness Analysis
* Sentence Consistency Analysis
* Repetition Detection
* Formality Analysis
* GPT-2 Perplexity Scoring

### Assessment Engine

* Preparedness Score Generation
* Response Classification

  * Natural Response
  * Prepared Response
  * Highly Structured Response
* Confidence Estimation
* Linguistic Trait Extraction

### Interactive Dashboard

* Streamlit-based user interface
* Real-time transcript display
* Metric visualization
* Response assessment dashboard

---

## System Architecture

Audio Input

↓

Speech Recording

↓

OpenAI Whisper

↓

Transcript Generation

↓

NLP Feature Extraction

* Vocabulary Richness
* Sentence Consistency
* Repetition Score
* Formality Score

↓

GPT-2 Perplexity Analysis

↓

Preparedness Scoring Engine

↓

Response Classification Dashboard

---

## Metrics Used

### Perplexity

Measures how predictable the transcript is according to a language model.

Lower perplexity often indicates highly structured or predictable language.

### Vocabulary Richness

Ratio of unique words to total words.

Higher values indicate greater lexical diversity.

### Sentence Consistency

Measures variation in sentence lengths.

Lower variation may indicate highly structured responses.

### Repetition Score

Measures repeated word usage throughout the transcript.

Higher repetition may indicate rehearsed language patterns.

### Formality Score

Measures occurrence of formal academic and professional language markers.

Examples:

* Therefore
* Furthermore
* Moreover
* Consequently
* Hence

---

## Technologies Used

### Machine Learning & NLP

* OpenAI Whisper
* GPT-2
* Transformers
* NumPy
* NLTK

### Backend

* Python

### Frontend

* Streamlit

### Audio Processing

* SoundDevice
* SciPy
* FFmpeg

---

## Example Output

Preparedness Score: 48/100

Response Type:
Prepared Response

Observed Characteristics:

* Rich Vocabulary
* Academic / Formal Language
* Highly Predictable Text

---

## Future Improvements

* N-Gram Repetition Analysis
* Semantic Similarity Analysis
* Speech Timing Features
* Eye Gaze Integration
* Head Pose Integration
* Multi-Modal Interview Assessment
* Emotion Recognition Features
* Behavioral Pattern Analysis

---

## Project Motivation

This project was developed to explore practical applications of:

* Speech Recognition
* Natural Language Processing
* Transcript Analytics
* Human Response Assessment
* AI-Powered Interview Technologies

The goal is to create a transparent and explainable transcript intelligence system based on measurable linguistic characteristics rather than unsupported AI-detection claims.

---

## Author

Shivaaya Pangasa

B.Tech Artificial Intelligence

AI Engineering Intern

GitHub: https://github.com/ShivaayaPangasa
