import google.generativeai as genai
import json
from typing import Dict, Any, List

# [SECURITY] Advanced Model Configuration with Safety Filters
SAFETY_SETTINGS = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]

def get_agent_tools() -> List[Any]:
    """[TECHNICAL] Defines native Python functions for autonomous tool-use."""
    return [] 

def get_agent_model(selected_state: str, safety_principles: str, tools: List[Any] = None) -> genai.GenerativeModel:
    """[ARCHITECTURE] Configures Gemini with System Instructions and Safety Filters."""
    return genai.GenerativeModel(
        model_name='gemini-2.0-flash',
        tools=tools,
        system_instruction=f"You are the National Election Safety Agent for {selected_state}. {safety_principles}. Use tools for data verification.",
        generation_config={
            "temperature": 0.2,
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 1024,
        },
        safety_settings=SAFETY_SETTINGS
    )

def start_agent_chat(model: genai.GenerativeModel, history: List[Dict[str, Any]] = None) -> genai.ChatSession:
    """[CORE] Starts a persistent chat session with internal memory."""
    return model.start_chat(history=history or [])
