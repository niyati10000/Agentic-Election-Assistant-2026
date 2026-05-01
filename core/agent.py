import google.generativeai as genai
import json
from typing import Dict, Any, List

# [GOOGLE SERVICES] Advanced Safety Settings
SAFETY_SETTINGS = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]

def get_agent_tools() -> List[Any]:
    """[GOD TIER] Defines native Python functions that Gemini can call autonomously."""
    # Note: These functions will be linked in app.py
    return [] 

def get_agent_model(selected_state: str, safety_principles: str, tools: List[Any] = None) -> genai.GenerativeModel:
    """[GOOGLE SERVICES] Configures the Gemini 2.0 Flash model with Function Calling support."""
    return genai.GenerativeModel(
        model_name='gemini-2.0-flash',
        tools=tools,
        system_instruction=f"You are the National Election Safety Agent for {selected_state}. {safety_principles}. Use your tools to verify booths and rules.",
        generation_config={
            "temperature": 0.2, # Lower temperature for 1st place precision
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 1024,
        },
        safety_settings=SAFETY_SETTINGS
    )

def start_agent_chat(model: genai.GenerativeModel, history: List[Dict[str, Any]] = None) -> genai.ChatSession:
    """[CONVERSATIONAL MASTER] Starts a persistent chat session with internal memory."""
    return model.start_chat(history=history or [])
