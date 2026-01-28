import core.state as state

def run_learning_assistant(user_input: str) -> str:
    context = state.vector_store.retrieve(user_input)

    prompt = f"""
Context:
{context}

User Question:
{user_input}
"""

    return state.crew.kickoff(inputs={"input": prompt})
