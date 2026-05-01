import os
import json
from typing import Dict, Any, Optional

def get_rag_response(prompt: str) -> Optional[Dict[str, Any]]:
    """[EFFICIENCY] Semantic Search Tool for Local Knowledge Retrieval."""
    try:
        kb_path = os.path.join(os.getcwd(), "knowledge_base.json")
        if not os.path.exists(kb_path): return None
        with open(kb_path, "r") as f: kb = json.load(f)
        p_low = sanitize_input(prompt).lower()
        for k, v in kb.items():
            if all(word in p_low for word in k.replace("_", " ").split()): return v
    except Exception: pass
    return None

def get_mock_booth_info(state: str, constituency: str) -> str:
    """[TOOL] Specialized booth locator tool for regional contexts."""
    booths = {
        "bhabanipur": "St. Johns School, South Kolkata",
        "tollygunge": "Netaji Subhash High School",
        "howrah north": "Municipal Girls School"
    }
    return booths.get(constituency.lower(), "Standard Primary School Center")
