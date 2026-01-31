from crewai import Agent, Task, Crew, Process

def create_learning_crew(
    user_input: str,
    mcp_context: dict | None = None,
    retry_instruction: str | None = None
) -> Crew:
    """
    CrewAI 0.5.0–compatible crew creation.
    All inputs are embedded directly into the task prompt.
    """

    agent = Agent(
        role="Tutor",
        goal="Answer the user's query accurately and helpfully.",
        backstory="You are a professional, calm, and precise AI tutor.",
        verbose=True
    )

    # Build task prompt safely
    task_prompt = f"""
User question:
{user_input}
"""

    if mcp_context:
        task_prompt += f"""

Context:
{mcp_context}
"""

    if retry_instruction:
        task_prompt += f"""

IMPORTANT:
{retry_instruction}
"""

    task = Task(
        description=task_prompt,
        expected_output="A clear, accurate answer to the user.",
        agent=agent
    )

    crew = Crew(
        agents=[agent],
        tasks=[task],
        process=Process.sequential,
        verbose=True
    )

    return crew
