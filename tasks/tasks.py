from crewai import Task, Crew, Process
from agents.agents import (
    language_intent_agent,
    code_intelligence_agent,
    teaching_agent
)

# --------------------------------------------------
# TASK 1: Intent Analysis (The Profiler)
# --------------------------------------------------
detect_intent_task = Task(
    description=(
        "Analyze user input: '{user_input}'\n"
        "Previous conversation context: {conversation_history}\n\n"
        "CLASSIFICATION:\n"
        "1. primary_intent: [concept_explanation|code_debug|code_review|optimization|best_practices|comparison]\n"
        "2. subject_domain: [python|javascript|algorithms|system_design|general_cs]\n"
        "3. complexity_indicators: [syntax|algorithmic|architectural]\n\n"
        "PEDAGOGICAL ASSESSMENT:\n"
        "4. assessed_level: Beginner|Intermediate|Advanced (based on vocabulary, question structure)\n"
        "5. knowledge_gaps: List prerequisites they probably don't know\n"
        "6. learning_style_signal: [example_driven|theory_first|hands_on]\n\n"
        "OUTPUT (Strict JSON):\n"
        "{{\n"
        '  "primary_intent": "...",\n'
        '  "subject_domain": "...",\n'
        '  "assessed_level": "...",\n'
        '  "prerequisites_needed": ["..."],\n'
        '  "inferred_goal": "what they really want to achieve",\n'
        '  "teaching_strategy": "scaffold|socratic|direct"\n'
        "}}"
    ),
    expected_output="JSON classification with pedagogical metadata. No user-facing text.",
    agent=language_intent_agent
)

# --------------------------------------------------
# TASK 2: Code Intelligence (The Analyzer)
# --------------------------------------------------
code_intelligence_task = Task(
    description=(
        "Analyze input: '{user_input}'\n"
        "User level from previous analysis: {{detect_intent_task.output}}\n\n"
        
        "IF NO CODE DETECTED:\n"
        "Return: {{'has_code': false}}\n\n"
        
        "IF CODE DETECTED:\n"
        "Perform analysis ADAPTED to user level detected above.\n\n"
        "For BEGINNER:\n"
        "- Syntax errors only\n"
        "- Basic PEP 8 violations\n"
        "- Simple idioms (list vs loop)\n"
        "- Explain errors in plain English\n\n"
        
        "For INTERMEDIATE:\n"
        "- Algorithmic complexity (Big O)\n"
        "- Pythonic patterns (comprehensions, generators)\n"
        "- Error handling gaps\n"
        "- Type hint suggestions\n\n"
        
        "For ADVANCED:\n"
        "- Concurrency issues (GIL, async/await, race conditions)\n"
        "- Memory optimization (slots, __slots__, weakref)\n"
        "- Design patterns and architecture\n"
        "- Trade-off analysis (speed vs memory vs readability)\n\n"
        
        "OUTPUT FORMAT (JSON):\n"
        "{{\n"
        '  "has_code": true,\n'
        '  "language": "python|javascript|...",\n'
        '  "analysis_depth": "beginner|intermediate|advanced",\n'
        '  "critical_issues": [\n'
        '    {{\n'
        '      "line": "...",\n'
        '      "severity": "error|warning|info",\n'
        '      "issue": "description",\n'
        '      "fix": "corrected code",\n'
        '      "concept": "what they need to learn to avoid this"\n'
        "    }}\n"
        "  ],\n"
        '  "optimization_opportunities": [...],\n'
        '  "complexity_analysis": "O(n) vs O(n²) explanation",\n'
        '  "teaching_focus": "what concept to emphasize"\n'
        "}}"
    ),
    expected_output="Structured JSON analysis adapted to user level, or empty object if no code.",
    agent=code_intelligence_agent,
    context=[detect_intent_task]
)

# --------------------------------------------------
# TASK 3: Adaptive Teaching (The Synthesizer)
# --------------------------------------------------
teaching_task = Task(
    description=(
        "Create personalized response to: '{user_input}'\n\n"
        
        "CONTEXT:\n"
        "- Knowledge Graph: {knowledge_graph}\n"
        "- Mastery Data: {mastery_data}\n"
        "- Retry Instruction (if any): {retry_instruction}\n\n"
        
        "The previous analyses have determined the user's intent, level, and whether "
        "they provided code. Use that context to personalize your response.\n\n"
        
        "RESPONSE STRATEGY:\n\n"
        "CASE A: CODE WITH ERRORS\n"
        "1. Acknowledge their attempt positively\n"
        "2. Point to specific error found\n"
        "3. Explain the CONCEPT behind the error (not just fix syntax)\n"
        "4. Show corrected code with inline comments\n"
        "5. Ask: 'Looking at line X, can you see why [concept] caused this?'\n\n"
        
        "CASE B: CODE OPTIMIZATION\n"
        "1. Validate their current approach\n"
        "2. Explain complexity trade-offs using Big O\n"
        "3. Present optimized solution as alternative\n"
        "4. Discuss: 'When would the simple version be better?'\n\n"
        
        "CASE C: CONCEPT QUESTION\n"
        "1. Check prerequisites and adapt to user level (Beginner/Intermediate/Advanced)\n"
        "2. If gap found: 'Before X, let's ensure Y is clear...'\n"
        "3. Use Socratic method: Ask 2-3 guiding questions before explanation\n"
        "4. Connect to previous knowledge from knowledge graph\n\n"
        
        "TONE RULES:\n"
        "- Match assessed_level (use context from previous analyses)\n"
        "- Beginners: Use analogies\n"
        "- Intermediate: Use technical terms with brief explanations\n"
        "- Advanced: Focus on edge cases and trade-offs\n\n"
        "ABSOLUTE PROHIBITIONS:\n"
        "- Never output JSON or raw analysis data\n"
        "- Never say 'The system detected...' or 'According to analysis...'\n"
        "- Always end with ONE specific follow-up question\n\n"
        "USER ASKED: {user_input}"
    ),
    expected_output="Natural, pedagogically-sound response ending with a follow-up question.",
    agent=teaching_agent,
    context=[detect_intent_task, code_intelligence_task]
)

# --------------------------------------------------
# CREW CONFIGURATION
# --------------------------------------------------
def create_learning_crew():
    return Crew(
        agents=[language_intent_agent, code_intelligence_agent, teaching_agent],
        tasks=[detect_intent_task, code_intelligence_task, teaching_task],
        process=Process.sequential,
        memory=False,  # CHANGED: Disabled to prevent slow memory saves (using custom memory instead)
        verbose=True,
        max_rpm=100
    )