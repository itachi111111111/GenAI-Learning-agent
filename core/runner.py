# core/runner.py
from core.state import crew, vector_store

def run_learning_assistant(user_input: str) -> str:
    context = vector_store.retrieve(user_input)

    prompt = f"""
    Context:
    {context}

    User Question:
    {user_input}
    """

    response = crew.kickoff(inputs={"input": prompt})
    return response
