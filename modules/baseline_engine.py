"""
==========================================================
Candidate Baseline Engine

Version 2

Generates a candidate-specific linguistic baseline
using all interview responses.

This baseline is later used for:

• Outlier Detection
• AI Flagging
• Adaptive Thresholds
• Interview Assessment

==========================================================
"""

from modules.interview_models import InterviewSession

import statistics


def generate_candidate_baseline(
    session: InterviewSession
):
    """
    Computes average linguistic metrics
    across an interview session.
    """
    
    perplexities = []
    
    vocabularies = []
    
    repetitions = []
    
    formalities = []
    
    consistencies = []



    for response in session.responses:

        if response.metrics is None:

            continue
        
        perplexities.append(response.metrics["perplexity"])
        
        vocabularies.append(response.metrics["vocabulary_richness"])
        
        repetitions.append(response.metrics["repetition_score"])
        
        formalities.append(response.metrics["formality_score"])
        
        consistencies.append(response.metrics["sentence_consistency"])
        
    if len(perplexities) == 0:
        
        return None
    
    baseline = {
        
        "perplexity": {
            "mean": round(
                statistics.mean(perplexities),
                2
            ),
            
            "std": round(
                statistics.stdev(perplexities),
                2
            ) if len(perplexities) > 1 else 0
        },
        
        "vocabulary": {
            "mean": round(
                statistics.mean(vocabularies),
                3
            ),
            
            "std": round(
                statistics.stdev(vocabularies),
                3
            ) if len(vocabularies) > 1 else 0
        },
        
        "repetition": {
            "mean": round(
                statistics.mean(repetitions),
                3
            ),
            
            "std": round(
                statistics.stdev(repetitions),
                3
            ) if len(repetitions) > 1 else 0
        },
        
        "formality": {
            "mean": round(
                statistics.mean(formalities),
                3
            ),
            
            "std": round(
                statistics.stdev(formalities),
                3
            ) if len(formalities) > 1 else 0
        },
        
        "consistency": {
            "mean": round(
                statistics.mean(consistencies),
                3
            ),
            
            "std": round(
                statistics.stdev(consistencies),
                3
            ) if len(consistencies) > 1 else 0
        },
        
        "responses_used": len(perplexities)
    }

    return baseline