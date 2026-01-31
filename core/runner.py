from dotenv import load_dotenv
load_dotenv()

from memory.follow_up_memory import FollowUpMemory
from crew import create_learning_crew
from protocols.mcp import MCPContext
from protocols.a2a import A2AChannel
from memory.memory_manager import retrieve_context, store_interaction

follow_up_memory = FollowUpMemory()
a2a_channel = A2AChannel()

def has_follow_up(response: str) -> bool:
    return response.strip().endswith("?")

def run_learning_assistant(user_input: str) -> str:
    # ---- Memory decay & update ----
    follow_up_memory.decay()
    follow_up_memory.update(user_input)

    # ---- MCP context ----
    mcp = MCPContext(user_input)
    memory = retrieve_context(user_input)
    mcp.attach_memory(memory)

    last_follow_up = follow_up_memory.get_preference()
    if last_follow_up:
        mcp.attach_signal("follow_up_preference", last_follow_up)

    # ✅ FIX IS HERE
    crew = create_learning_crew(user_input)

    result = crew.kickoff(inputs={
        "user_input": user_input,
        "mcp_context": mcp.export_for_llm()
    })

    output = str(result)

    # ---- Enforce follow-up ----
    if not has_follow_up(output):
        result = crew.kickoff(inputs={
            "user_input": user_input,
            "mcp_context": mcp.export_for_llm(),
            "retry_instruction": (
                "Your previous response was missing the required follow-up question. "
                "Re-answer fully and end with EXACTLY ONE short, neutral follow-up."
            )
        })
        output = str(result)

    # ---- Persist memory ----
    follow_up_memory.store_from_response(output)
    store_interaction(user_input, output)

    return output
