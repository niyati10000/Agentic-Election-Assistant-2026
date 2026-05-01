import streamlit as st
import google.generativeai as genai
import os
import sys
import datetime
import time
from typing import Dict, Any, Tuple, Optional

# Import Modularized Components
from core.agent import get_agent_model, execute_agent_reasoning
from utils.tools import sanitize_input, get_rag_response, get_mock_booth_info
from ui.styles import apply_custom_styles, generate_mermaid_mission, generate_voter_slip
from dotenv import load_dotenv

# --- Initialization ---
load_dotenv()
apply_custom_styles()

# [SECURITY] Professional API Key Management
API_KEY: Optional[str] = None
try:
    API_KEY = st.secrets.get("GOOGLE_API_KEY") or os.getenv("GOOGLE_API_KEY")
except Exception:
    API_KEY = os.getenv("GOOGLE_API_KEY")

if API_KEY:
    genai.configure(api_key=API_KEY)
else:
    if "streamlit" in sys.modules:
        st.error("🛑 GOOGLE_API_KEY Missing. Please check Streamlit Secrets.")
        st.stop()

# --- Configuration & Data ---
AI_SAFETY_PRINCIPLES = "Neutrality: No political bias. Accuracy: Use verified ECI rules only. Responsibility: Include safety confidence."

ELECTION_DATA: Dict[str, Dict[str, str]] = {
    "West Bengal": {"Phase 2": "April 29, 2026", "Status": "Polling Phase 2", "Helpline": "1950 (WB)"},
    "Tamil Nadu": {"Status": "Polling Completed", "Helpline": "1950 (TN)"},
    "Kerala": {"Status": "Polling Completed", "Helpline": "1950 (KL)"}
}

# --- UI Components ---

def render_sidebar() -> Tuple[str, bool, str]:
    with st.sidebar:
        st.image("election_hero.png", width=None, caption="Election Safety Guard")
        st.title("Control Center")
        state = st.selectbox("🌍 State Context:", list(ELECTION_DATA.keys()))
        lang = st.radio("🌐 Language:", ["English", "हिंदी", "বাংলা"], help="[ACCESSIBILITY] Multilingual support for inclusive voting.")
        
        st.divider()
        st.subheader("⚙️ Mission Settings")
        rag_mode = st.toggle("Advanced RAG Retrieval", value=True)
        
        st.divider()
        st.subheader("📊 System Telemetry")
        if "agent_logs" in st.session_state:
            for log in reversed(st.session_state.agent_logs[-5:]):
                st.markdown(f"<div class='agent-log'>[{log['tag']}] {log['message']}</div>", unsafe_allow_html=True)
                
        if st.button("Reset Session"):
            st.session_state.messages = []
            st.session_state.agent_logs = []
            st.rerun()
    return state, rag_mode, lang

def log_agent_action(tag: str, message: str) -> None:
    if "agent_logs" not in st.session_state: st.session_state.agent_logs = []
    st.session_state.agent_logs.append({"timestamp": datetime.datetime.now().strftime("%H:%M:%S"), "tag": tag, "message": message})

# --- Main App Logic ---

def main() -> None:
    selected_state, rag_mode, selected_lang = render_sidebar()
    st.title("🛡️ National Election Safety Agent")
    st.caption(f"Context: {selected_state} | Language: {selected_lang} | Model: Gemini 2.0 Flash")

    if "messages" not in st.session_state: st.session_state.messages = []

    # Chat Display
    for m in st.session_state.messages:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])
            if "artifact" in m and m["artifact"]: st.markdown(m["artifact"], unsafe_allow_html=True)
            if "mermaid" in m: st.mermaid(m["mermaid"])

    # Input Logic
    if prompt := st.chat_input("How can I assist your voting mission today?"):
        prompt = sanitize_input(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)

        with st.chat_message("assistant"):
            start_time = time.time()
            with st.status("🏗️ Orchestrating Multi-Agent Logic...", expanded=True) as status:
                
                log_agent_action("THINK", f"Analyzing request for {selected_state} in {selected_lang}.")
                
                # Step 1: Semantic RAG Cache
                if rag_mode:
                    cached = get_rag_response(prompt)
                    if cached:
                        latency = round(time.time() - start_time, 3)
                        log_agent_action("RAG", f"HIT: Semantic cache used. Latency: {latency}s")
                        display_text = f"⚖️ **Rulebook Check:**\n{cached['legal']}\n\n🚀 **Plan:**\n{cached['advice']}\n\n<div class='confidence-badge'>Confidence: {cached['score']}</div>"
                        st.markdown(display_text, unsafe_allow_html=True)
                        
                        mission_map = generate_mermaid_mission(cached.get("const", "Region"), ELECTION_DATA[selected_state]["Status"])
                        st.mermaid(mission_map)
                        
                        v_slip = generate_voter_slip("Voter", selected_state, cached.get("booth", "N/A"), cached.get("const", "N/A"))
                        st.markdown(v_slip, unsafe_allow_html=True)
                        
                        st.session_state.messages.append({"role": "assistant", "content": display_text, "artifact": v_slip, "mermaid": mission_map})
                        status.update(label=f"✅ Mission Complete ({latency}s)", state="complete")
                        return

                # Step 2: Advanced Gemini Execution
                try:
                    model = get_agent_model(selected_state, AI_SAFETY_PRINCIPLES)
                    res = execute_agent_reasoning(model, prompt, ELECTION_DATA[selected_state])
                    
                    latency = round(time.time() - start_time, 3)
                    log_agent_action("GEMINI", f"JSON Reasoner Complete. Latency: {latency}s")
                    
                    display_text = f"⚖️ **Rulebook Check:**\n{res['legal_check']}\n\n🚀 **Plan:**\n{res['safety_mission']}\n\n<div class='confidence-badge'>🛡️ Confidence: {res['confidence']}</div>"
                    st.markdown(display_text, unsafe_allow_html=True)
                    
                    v_slip = None
                    if res.get("requires_voter_slip"):
                        v_slip = generate_voter_slip("Voter", selected_state, "Primary Center", "General")
                        st.markdown(v_slip, unsafe_allow_html=True)

                    mission_map = generate_mermaid_mission("General Area", ELECTION_DATA[selected_state]["Status"])
                    st.mermaid(mission_map)
                    
                    st.session_state.messages.append({"role": "assistant", "content": display_text, "mermaid": mission_map, "artifact": v_slip})
                    status.update(label=f"✅ Mission Complete ({latency}s)", state="complete")
                    
                except Exception as e:
                    st.error(f"Reasoning Failed: {e}")
                    log_agent_action("FATAL", str(e))

if __name__ == "__main__":
    main()
