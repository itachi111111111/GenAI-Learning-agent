from crewai import Crew, Process

from agents.agents import (
    language_intent_agent,
    code_intelligence_agent,
    teaching_agent,
    execution_simulation_agent,
    verifier_agent
)

from tasks.tasks import (
    detect_intent_task,
    code_intelligence_task,
    teaching_task
)


def create_learning_crew():
    return Crew(
        agents=[
            language_intent_agent,
            code_intelligence_agent,
            teaching_agent,
            execution_simulation_agent,
            verifier_agent
        ],
        tasks=[
            detect_intent_task,          # silent intent analysis
            code_intelligence_task,      # silent deep code analysis
            teaching_task                # ONLY user-facing output
        ],
        process=Process.sequential,
        verbose=True
    )

