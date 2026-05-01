import google.generativeai as genai
import json
from typing import Dict, Any

# [GOOGLE SERVICES] Advanced Safety Settings for Responsible AI (RAI)
SAFETY_SETTINGS = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]

def get_agent_model(selected_state: str, safety_principles: str) -> genai.GenerativeModel:
    """[GOOGLE SERVICES] Configures the Gemini 2.0 Flash model with System Instructions and Safety Settings."""
    return genai.GenerativeModel(
        model_name='gemini-2.0-flash',
        system_instruction=f"You are the National Election Safety Agent for {selected_state}. {safety_principles}",
        generation_config={
            "response_mime_type": "application/json",
            "response_schema": {
                "type": "object",
                "properties": {
                    "legal_check": {"type": "string"},
                    "safety_mission": {"type": "string"},
                    "confidence": {"type": "string"},
                    "requires_voter_slip": {"type": "boolean"}
                },
                "required": ["legal_check", "safety_mission", "confidence"]
            }
        },
        safety_settings=SAFETY_SETTINGS
    )

def execute_agent_reasoning(model: genai.GenerativeModel, prompt: str, context: Dict[str, Any]) -> Dict[str, Any]:
    """[CORE] Executes the Multi-Agent reasoning loop and returns structured results."""
    full_prompt = f"Context: {json.dumps(context)}\nUser Query: \"{prompt}\"\nProvide structured response."
    response = model.generate_content(full_prompt)
    return json.loads(response.text)
