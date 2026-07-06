from modules.interview_models import InterviewResponse, InterviewSession

# Create one interview response
response = InterviewResponse(
    question="What is overfitting?",
    answer="Overfitting occurs when a model memorizes the training data."
)

# Create an interview session
session = InterviewSession(
    candidate_name="John Doe",
    interview_id="INT001"
)

# Add the response to the interview
session.responses.append(response)

print(session)