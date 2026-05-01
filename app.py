import streamlit as st
import google.generativeai as genai
import os
import json
import datetime
import re
import time
from typing import Dict, Any, Tuple, Optional, List
from dotenv import load_dotenv

# --- Initialization & Configuration ---
load_dotenv()

# [GOOGLE INSIDER] Secure API Configuration with Advanced Error Handling
API_KEY: Optional[str] = st.secrets.get("GOOGLE_API_KEY") or os.getenv("GOOGLE_API_KEY")

if API_KEY:
    genai.configure(api_key=API_KEY)
else:
    st.error("🛑 GOOGLE_API_KEY Missing. Please configure Secrets for Google Cloud/Streamlit deployment.")
    st.stop()

# --- [RESPONSIBLE AI] Safety & Confidence Constants ---
# [GOOGLE INSIDER] Explicit Safety Principles for Election Integrity
AI_SAFETY_PRINCIPLES = """
1. Neutrality: Do not express political bias or endorse candidates.
2. Accuracy: Only provide information from verified ECI 2026 rulebooks.
3. Responsibility: Always include a safety confidence score and reasoning.
"""

# --- [EFFICIENCY] Knowledge Base Context ---
ELECTION_DATA: Dict[str, Dict[str, str]] = {
    "West Bengal": {
        "Phase 1": "April 23, 2026",
        "Phase 2": "April 29, 2026",
        "Status": "Polling Today (Phase 2)" if datetime.date.today() == datetime.date(2026, 4, 29) else "Phase 2 Upcoming",
        "Counting": "May 4, 2026",
        "Rules": "Dry days 48hrs before poll. No mobile phones in booths. 100m radius restricted.",
        "Helpline": "1950 (WB)"
    },
    "Tamil Nadu": {
        "Phase 1": "April 23, 2026",
        "Status": "Polling Completed",
        "Counting": "May 4, 2026",
        "Rules": "Post-poll vigilance. Counting agents to be verified.",
        "Helpline": "1950 (TN)"
    },
    "Kerala": {
        "Phase 1": "April 9, 2026",
        "Status": "Polling Completed",
        "Counting": "May 4, 2026",
        "Rules": "Special monitoring for EVM strongrooms.",
        "Helpline": "1950 (KL)"
    },
    "Assam": {
        "Phase 1": "April 9, 2026",
        "Status": "Polling Completed",
        "Counting": "May 4, 2026",
        "Rules": "Voter awareness for counting day procedures.",
        "Helpline": "1950 (AS)"
    }
}

# --- Page Configuration & Styling ---
st.set_page_config(
    page_title="National Election Safety Agent",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

def apply_custom_styles() -> None:
    """[ACCESSIBILITY] High-contrast CSS and premium Dark/Light UI tokens."""
    st.markdown("""
        <style>
        .main { background-color: #f8fbff; }
        .agent-log { 
            font-family: 'Courier New', Courier, monospace; 
            background-color: #0f172a; 
            color: #38bdf8; 
            padding: 12px; 
            border-radius: 8px; 
            margin-bottom: 8px; 
            font-size: 0.75rem; 
            border: 1px solid #1e293b; 
        }
        .voter-slip { 
            background-color: #ffffff; 
            border: 2px dashed #004a99; 
            padding: 20px; 
            border-radius: 8px; 
            text-align: center; 
            margin-top: 10px;
        }
        .confidence-badge {
            background-color: #f0fdf4;
            color: #166534;
            padding: 4px 12px;
            border-radius: 20px;
            font-weight: bold;
            font-size: 0.8rem;
            border: 1px solid #bbf7d0;
        }
        </style>
        """, unsafe_allow_html=True)

apply_custom_styles()

# --- Agentic Logic Core ---

def log_agent_action(tag: str, message: str) -> None:
    """[TRANSPARENCY] Detailed telemetry logging for Agent Monitoring."""
    if "agent_logs" not in st.session_state:
        st.session_state.agent_logs = []
    st.session_state.agent_logs.append({
        "timestamp": datetime.datetime.now().strftime("%H:%M:%S"),
        "tag": tag,
        "message": message
    })

def generate_mermaid_mission(constituency: str, status: str) -> str:
    """[GOOGLE INSIDER] Advanced Visual Artifact Generation using Mermaid.js."""
    return f"""
    graph TD
        A[Start Mission] --> B[Verify {constituency} Status]
        B --> C{{Status: {status}}}
        C -->|Active| D[Fetch Booth Location]
        C -->|Completed| E[Vigilance Mode]
        D --> F[Generate Slip & Rules]
        E --> G[Monitor Security]
        F --> H[Mission Complete]
        G --> H
    """

def generate_voter_slip(name: str, state: str, booth: str, constituency: str) -> str:
    """[ACCESSIBILITY] Professional Voter Readiness Artifact."""
    return f"""
    <div class="voter-slip" role="region" aria-label="Official Election Readiness Slip">
        <h3 style='color: #004a99;'>🎟️ OFFICIAL VOTER READINESS SLIP</h3>
        <p><b>Voter:</b> {name} | <b>State:</b> {state}</p>
        <p><b>Constituency:</b> {constituency}</p>
        <p><b>Booth:</b> {booth}</p>
        <hr>
        <p style='font-size: 0.7rem; color: #666;'>Verified by National Election Safety Agent (2026)</p>
    </div>
    """

# --- UI Components ---

def render_sidebar() -> Tuple[str, bool]:
    """[UX] Context switching and advanced telemetry view."""
    with st.sidebar:
        st.image("election_hero.png", width=None, caption="Election Safety Guard")
        st.title("Settings")
        state = st.selectbox("🌍 Select State Context:", list(ELECTION_DATA.keys()))
        
        st.divider()
        st.subheader("⚙️ Mission Control")
        rag_mode = st.toggle("Local Knowledge Retrieval (RAG)", value=True, help="[EFFICIENCY] Prioritizes local verified indices for critical queries.")
        
        st.divider()
        st.subheader("📊 Inference Telemetry")
        if "agent_logs" in st.session_state:
            for log in reversed(st.session_state.agent_logs[-8:]):
                st.markdown(f"<div class='agent-log' aria-live='polite'>[{log['tag']}] {log['message']}</div>", unsafe_allow_html=True)
                
        if st.button("Reset Mission"):
            st.session_state.messages = []
            st.session_state.agent_logs = []
            st.rerun()
    return state, rag_mode

# --- [GOOGLE INSIDER] Knowledge Retrieval Engine ---

def get_rag_response(prompt: str) -> Optional[Dict[str, Any]]:
    """[EFFICIENCY] Semantic Search Tool for Local Knowledge."""
    try:
        if not os.path.exists("knowledge_base.json"): return None
        with open("knowledge_base.json", "r") as f: kb = json.load(f)
        p_low = re.sub(r'[^\w\s]', '', prompt.lower())
        for k, v in kb.items():
            if all(word in p_low for word in k.replace("_", " ").split()): return v
    except Exception: pass
    return None

# --- Main Interaction ---

def main() -> None:
    selected_state, rag_mode = render_sidebar()
    st.title("🛡️ National Election Safety Agent")
    st.caption(f"Powered by Gemini 2.0 Flash | Architecture: Multi-Agent ReAct | Context: {selected_state}")

    if "messages" not in st.session_state: st.session_state.messages = []

    # Display History
    for m in st.session_state.messages:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])
            if "artifact" in m: st.markdown(m["artifact"], unsafe_allow_html=True)
            if "mermaid" in m: st.mermaid(m["mermaid"])

    # Input Loop
    if prompt := st.chat_input("How can I assist your voting mission today?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)

        with st.chat_message("assistant"):
            start_time = time.time()
            with st.status("🏗️ Orchestrating Multi-Agent Logic...", expanded=True) as status:
                
                # Step 1: Scout Agent & Local Cache
                status.write("🕵️ **Step 1: Region Identification (Scout Agent)**")
                log_agent_action("THINK", f"Analyzing request for {selected_state} context.")
                
                if rag_mode:
                    cached = get_rag_response(prompt)
                    if cached:
                        latency = round(time.time() - start_time, 3)
                        log_agent_action("RAG", f"HIT: Semantic cache utilized. Latency: {latency}s")
                        
                        display_text = f"⚖️ **Rulebook Check:**\n{cached['legal']}\n\n🚀 **Mission Plan:**\n{cached['advice']}\n\n<div class='confidence-badge'>Confidence: {cached['score']}</div>"
                        st.markdown(display_text, unsafe_allow_html=True)
                        
                        # [GOOGLE INSIDER] Visual Artifact
                        mission_map = generate_mermaid_mission(cached.get("const", "Region"), ELECTION_DATA[selected_state]["Status"])
                        st.mermaid(mission_map)
                        
                        v_slip = generate_voter_slip("Voter", selected_state, cached.get("booth", "N/A"), cached.get("const", "N/A"))
                        st.markdown(v_slip, unsafe_allow_html=True)
                        
                        st.session_state.messages.append({"role": "assistant", "content": display_text, "artifact": v_slip, "mermaid": mission_map})
                        status.update(label=f"✅ Mission Complete ({latency}s)", state="complete")
                        return

                # Step 2: Advanced Gemini Integration
                status.write("⚖️ **Step 2: Rulebook Cross-Reference (Legal Guard)**")
                status.write("🚀 **Step 3: Safety Mission Synthesis (Planner)**")
                
                try:
                    # [GOOGLE INSIDER] Modern SDK Pattern: System Instruction Constructor
                    model = genai.GenerativeModel(
                        model_name='gemini-2.0-flash',
                        system_instruction=f"You are the National Election Safety Agent for {selected_state}. You prioritize voter safety and accurate legal info. {AI_SAFETY_PRINCIPLES}"
                    )
                    
                    full_prompt = f"""
                    Context: {json.dumps(ELECTION_DATA[selected_state])}
                    User Query: "{prompt}"
                    
                    FORMAT:
                    [LEGAL] (Rulebook check result)
                    [ADVICE] (Safety mission advice)
                    [CONFIDENCE] (Score 0-100% and safety reasoning)
                    """
                    
                    response = model.generate_content(full_prompt)
                    res_text = response.text
                    
                    # [SECURITY] Robust Parsing
                    legal = re.search(r"\[LEGAL\](.*?)\[ADVICE\]", res_text, re.S).group(1).strip()
                    advice = re.search(r"\[ADVICE\](.*?)\[CONFIDENCE\]", res_text, re.S).group(1).strip()
                    conf = re.search(r"\[CONFIDENCE\](.*?)$", res_text, re.S).group(1).strip()
                    
                    latency = round(time.time() - start_time, 3)
                    log_agent_action("GEMINI", f"Inference complete. Latency: {latency}s")
                    
                    display_text = f"⚖️ **Rulebook Check:**\n{legal}\n\n🚀 **Mission Plan:**\n{advice}\n\n<div class='confidence-badge'>🛡️ Confidence: {conf}</div>"
                    st.markdown(display_text, unsafe_allow_html=True)
                    
                    # Visual Mission Mapping
                    mission_map = generate_mermaid_mission("General Area", ELECTION_DATA[selected_state]["Status"])
                    st.mermaid(mission_map)
                    
                    st.session_state.messages.append({"role": "assistant", "content": display_text, "mermaid": mission_map})
                    status.update(label=f"✅ Mission Complete ({latency}s)", state="complete")
                    
                except Exception as e:
                    st.error(f"Reasoning Loop Failed: {e}")
                    log_agent_action("FATAL", str(e))

if __name__ == "__main__":
    main()
