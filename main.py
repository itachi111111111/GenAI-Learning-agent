from dotenv import load_dotenv
load_dotenv()

from memory.follow_up_memory import FollowUpMemory
from crew import create_learning_crew
from protocols.mcp import MCPContext
from protocols.a2a import A2AChannel
from memory.memory_manager import retrieve_context, store_interaction


# -------------------------------
# Follow-up preference memory
# -------------------------------
follow_up_memory = FollowUpMemory()


def has_follow_up(response: str) -> bool:
    response = response.strip()
    return response.endswith("?")


# Global A2A channel (internal only)
a2a_channel = A2AChannel()


def run_learning_assistant(user_input: str):
     # --- DECAY OLD FOLLOW-UP PREFERENCE ---
    follow_up_memory.decay()
    # --- UPDATE FOLLOW-UP MEMORY (from user reply) ---
    follow_up_memory.update(user_input)

    # --- MCP CONTEXT ---
    mcp = MCPContext(user_input)

    memory = retrieve_context(user_input)
    mcp.attach_memory(memory)

    # -------------------------------
    # STEP A — Retrieve last follow-up preference
    # -------------------------------
    last_follow_up = follow_up_memory.get_preference()
    if last_follow_up:
        mcp.attach_signal("follow_up_preference", last_follow_up)

    # --- CREW ---
    crew = create_learning_crew()

    # -------- FIRST PASS --------
    result = crew.kickoff(
        inputs={
            "user_input": user_input,
            "mcp_context": mcp.export_for_llm()  # dict ONLY
        }
    )

    output = str(result)

    # -------- SILENT SELF-RETRY (FOLLOW-UP ENFORCEMENT) --------
    if not has_follow_up(output):
        result = crew.kickoff(
            inputs={
                "user_input": user_input,
                "mcp_context": mcp.export_for_llm(),
                "retry_instruction": (
                    "Your previous response was missing the required follow-up question. "
                    "Re-answer fully and end with EXACTLY ONE short, neutral follow-up."
                )
            }
        )
        output = str(result)

    # -------------------------------
    # STEP B — Store the new follow-up type
    # -------------------------------
    follow_up_memory.store_from_response(output)

    # --- SILENT MEMORY UPDATE ---
    store_interaction(user_input, output)

    return output


if __name__ == "__main__":
    print("GenAI Personalized Learning Assistant (MCP + FAISS)")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            break

        print("\nAssistant:\n")
        print(run_learning_assistant(user_input))
        print("-" * 50)
