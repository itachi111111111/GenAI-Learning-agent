import json
import os
from datetime import datetime

from dotenv import load_dotenv
load_dotenv()

from tasks.tasks import create_learning_crew
from memory.follow_up_memory import FollowUpMemory
from memory.memory_manager import retrieve_context, store_interaction
from memory.knowledge_graph import (
    update_concept_mastery, 
    export_knowledge_graph
)

follow_up_memory = FollowUpMemory()

def has_follow_up(response: str) -> bool:
    return response.strip().endswith("?")

def run_learning_assistant(user_input: str) -> str:
    # Update memory
    follow_up_memory.decay()
    follow_up_memory.update(user_input)
    last_follow_up = follow_up_memory.get_preference()
    
    # Get knowledge context
    knowledge_graph_data = export_knowledge_graph()
    
    # Build inputs
    inputs = {
        "user_input": user_input,
        "conversation_history": "",  # Simplified
        "knowledge_graph": knowledge_graph_data,
        "mastery_data": knowledge_graph_data,
        "retry_instruction": last_follow_up if last_follow_up else ""
    }
    
    # Create and run crew
    crew = create_learning_crew()
    
    try:
        result = crew.kickoff(inputs=inputs)
        
        # Extract the actual text output - CrewAI 1.9.3 returns object with 'raw' or string
        if hasattr(result, 'raw'):
            output = result.raw
        elif hasattr(result, 'output'):
            output = result.output
        else:
            output = str(result)
        
        # Simple concept tracking (avoid complex parsing)
        concepts = []
        if "loop" in user_input.lower():
            concepts.extend(["loops", "for loop", "while loop"])
        if "function" in user_input.lower():
            concepts.append("functions")
        
        # Update mastery (simple)
        for concept in concepts:
            update_concept_mastery(concept, 0.7)
        
        # Enforce follow-up if missing
        if not has_follow_up(output):
            inputs["retry_instruction"] = (
                "Your previous response was missing the required follow-up question. "
                "Re-answer fully and end with EXACTLY ONE short follow-up."
            )
            crew = create_learning_crew()
            result = crew.kickoff(inputs=inputs)
            output = result.raw if hasattr(result, 'raw') else str(result)
        
        # Store interaction
        store_interaction(user_input, output)
        
        follow_up_memory.store_from_response(output)
        return output
        
    except Exception as e:
        print(f"Error in crew execution: {e}")
        import traceback
        traceback.print_exc()
        # Return a generic fallback instead of exposing errors
        return "I'm having trouble processing that right now. Could you try rephrasing your question?"

if __name__ == "__main__":
    result = run_learning_assistant("what is a loop in python?")
    print(result)