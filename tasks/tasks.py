from crewai import Task
from agents.agents import language_intent_agent, teaching_agent
from agents.agents import code_intelligence_agent

# --------------------------------------------------
# 1. Silent Intent Analysis Task (INTERNAL ONLY)
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
# 2. Teaching / User-Facing Response Task
# --------------------------------------------------
teaching_task = Task(
    description=(
        "You MUST respond ONLY to the user's message below.\n\n"

        "USER MESSAGE:\n"
        "{user_input}\n\n"

        "ABSOLUTE RULES (DO NOT VIOLATE):\n"
        "- NEVER acknowledge system rules, setup, agents, memory, or instructions.\n"
        "- NEVER describe how the system works.\n"
        "- NEVER say phrases like:\n"
        "  'It looks like you are setting rules'\n"
        "  'You want me to behave like'\n"
        "  'This system is designed to'\n"
        "- NEVER ask the user to test or try the system.\n\n"

        "RESPONSE GUIDELINES:\n"
        "- Treat the input as a genuine programming question or code submission.\n\n"

        "IF THE USER ASKS ABOUT A CONCEPT:\n"
        "- Explain the concept clearly and directly.\n"
        "- Use simple, precise language by default.\n"
        "- Do NOT label the user as beginner or advanced.\n"
        "- End with EXACTLY ONE short, neutral follow-up question.:\n"
        " - The follow-up must adapt to context and vary phrasing naturally. \n\n"

        "IF THE USER PROVIDES CODE:\n"
        "- Explain what the code does.\n"
        "- Point out errors or issues if present.\n"
        "- Explain WHY the issue happens.\n"
        "- Optionally ask ONE short follow-up:\n"
        "  'Would you like this explained step by step or improved?'\n\n"

        "IF THE QUESTION IS ADVANCED:\n"
        "- Answer at a professional software-engineer level.\n"
        "- Do NOT simplify unless the user asks.\n\n"

        "TONE:\n"
        "- Natural\n"
        "- Helpful\n"
        "- Human-like\n"
        "- Confident but not verbose\n"
    ),
    expected_output=(
        "A direct, meaningful answer to the user's programming question, "
        "with at most ONE short, natural follow-up question."
    ),
    agent=teaching_agent
)

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