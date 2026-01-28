from crew import create_learning_crew
from protocols.mcp import MCPContext
from memory.memory_manager import retrieve_context, store_interaction

def run_learning_assistant(user_input: str) -> str:
    mcp = MCPContext(user_input)

    memory = retrieve_context(user_input)
    mcp.attach_memory(memory)

    crew = create_learning_crew()

    result = crew.kickoff(
        inputs={
            "user_input": user_input,
            "mcp_context": mcp.export_for_llm()
        }
    )

    output = str(result)
    store_interaction(user_input, output)

    return output
