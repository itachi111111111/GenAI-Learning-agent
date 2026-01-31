from crewai import Agent, Task, Crew
from langchain_openai import ChatOpenAI
import os

def create_learning_crew():
    """
    Creates a CrewAI crew with placeholders for dynamic inputs.
    Returns a crewai.Crew instance.
    """
    
    # Initialize LLM (choose one based on your setup)
    llm = ChatOpenAI(
        model="gpt-4o-mini",  # or gpt-4, gpt-3.5-turbo
        api_key=os.getenv("OPENAI_API_KEY"),
        temperature=0.7
    )
    
    # Alternative: Use Groq for faster/cheaper inference
    # llm = ChatGroq(
    #     model="mixtral-8x7b-32768",
    #     api_key=os.getenv("GROQ_API_KEY")
    # )

    # Define the agent
    learning_agent = Agent(
        role='Adaptive Learning Assistant',
        goal='Provide personalized learning experiences and assess user understanding through follow-up questions',
        backstory="""You are an expert educational AI with years of experience in 
        personalized tutoring. You adapt to the user's knowledge level and learning style.
        You always verify understanding by asking exactly one follow-up question at the end.""",
        llm=llm,
        verbose=True,
        allow_delegation=False
    )

    # Define the task with PLACEHOLDERS (curly braces)
    # These will be replaced by kickoff(inputs={...})
    learning_task = Task(
        description="""You are helping a user learn. Analyze their input and provide an educational response.

USER INPUT: {user_input}

ADDITIONAL CONTEXT: {mcp_context}

{retry_instruction}

REQUIREMENTS:
1. Provide a comprehensive, accurate response to the user's query
2. Adapt the complexity based on the context provided
3. You MUST end your response with EXACTLY ONE short, neutral follow-up question to verify understanding
4. The follow-up question should be on a new line at the very end
5. Do not ask rhetorical questions - ask a genuine question that checks their comprehension""",
        expected_output="Educational response ending with exactly one follow-up question marked by a question mark at the end",
        agent=learning_agent
    )

    # Create and return the crew
    crew = Crew(
        agents=[learning_agent],
        tasks=[learning_task],
        verbose=True,
        process="sequential"  # or "hierarchical" if using manager
    )
    
    return crew