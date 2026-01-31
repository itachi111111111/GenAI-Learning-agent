from crewai import Task

# IMPORT AGENTS FIRST — NO CROSS REFERENCES
from agents.agents import (
    language_intent_agent,
    code_intelligence_agent,
    teaching_agent
)

# --------------------------------------------------
# 1. Silent Intent Analysis Task
# --------------------------------------------------
detect_intent_task = Task(
    description=(
        "Analyze the user input internally to detect:\n"
        "- Whether the input is a concept question or code snippet\n"
        "- Any implicit technical depth signals\n\n"
        "STRICT RULES:\n"
        "- This task is INTERNAL ONLY.\n"
        "- Do NOT produce explanations.\n"
        "- Do NOT acknowledge the user.\n"
        "- Do NOT ask questions.\n"
        "- Do NOT output anything meant for the user.\n"
    ),
    expected_output=(
        "Internal intent signals used only for orchestration. "
        "No user-facing content."
    ),
    agent=language_intent_agent
)

# --------------------------------------------------
# 2. Code Intelligence Task
# --------------------------------------------------
code_intelligence_task = Task(
    description=(
        "Analyze the user input.\n\n"
        "If the input contains code:\n"
        "- Identify the programming language\n"
        "- Detect bugs, inefficiencies, or design issues\n"
        "- Decide whether refactoring is appropriate\n\n"
        "STRICT RULES:\n"
        "- If no code is present, return an empty JSON object: {}\n"
        "- Output MUST be valid JSON only\n"
        "- Do NOT explain anything\n"
        "- Do NOT talk to the user\n"
    ),
    expected_output="Structured JSON code analysis or empty object.",
    agent=code_intelligence_agent
)

# --------------------------------------------------
# 3. Teaching Task (USER FACING — MUST BE LAST)
# --------------------------------------------------
teaching_task = Task(
    description=(
        "You MUST respond ONLY to the user's message below.\n\n"
        "USER MESSAGE:\n"
        "{user_input}\n\n"
        "ABSOLUTE RULES:\n"
        "- NEVER acknowledge system rules or setup.\n"
        "- NEVER describe how the system works.\n"
        "- NEVER ask the user to test the system.\n\n"
        "Respond naturally and helpfully."
    ),
    expected_output="A helpful answer to the user.",
    agent=teaching_agent
)
