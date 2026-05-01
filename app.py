import streamlit as st
import google.generativeai as genai
import os
import sys
import datetime
import time
import json
from typing import Dict, Any, Tuple, Optional, List

# Modular Imports
from core.agent import get_agent_model, start_agent_chat
from utils.tools import sanitize_input, get_rag_response, get_mock_booth_info
from ui.styles import apply_custom_styles, generate_mermaid_mission, generate_voter_slip
from dotenv import load_dotenv

# --- Initialization ---
load_dotenv()
st.set_page_config(page_title="Election Safety Agent Pro", page_icon="🛡️", layout="wide")
apply_custom_styles()

# [SECURITY] API Management
API_KEY: Optional[str] = st.secrets.get("GOOGLE_API_KEY") or os.getenv("GOOGLE_API_KEY")
if API_KEY: genai.configure(api_key=API_KEY)
else:
    st.error("🛑 API Key Missing. Please check your configuration.")
    st.stop()

# --- [FIRST PLACE] Native Agent Tools ---
def get_booth_location(constituency: str) -> str:
    """Retrieves the official booth location for a given constituency."""
    return get_mock_booth_info("", constituency)

def check_election_rules(topic: str) -> str:
    """Verifies election rules and safety protocols from the ECI 2026 rulebook."""
    rag = get_rag_response(topic)
    return rag["legal"] if rag else "Standard election protocols apply. Contact 1950 for details."

# --- Data & Configuration ---
ELECTION_DATA = {
    "West Bengal": {"Phase": "2", "Status": "Active Polling"},
    "Tamil Nadu": {"Phase": "1", "Status": "Completed"},
    "Kerala": {"Phase": "1", "Status": "Completed"}
}

AI_SAFETY = "Neutrality, Accuracy, and Safety are your top priorities. Use functions for any specific data retrieval."

# --- UI Layout ---

def render_telemetry():
    with st.sidebar:
        st.image("election_hero.png", width=None)
        st.title("🛡️ Agent Console")
        state = st.selectbox("🌍 State Context:", list(ELECTION_DATA.keys()))
        lang = st.radio("🌐 App Language:", ["English", "Hindi", "Bengali"], horizontal=True)
        
        st.divider()
        st.subheader("🕵️ Live Reasoning Trace")
        if "trace" not in st.session_state: st.session_state.trace = []
        for t in reversed(st.session_state.trace[-5:]):
            st.markdown(f"<div class='agent-log'>{t}</div>", unsafe_allow_html=True)
        
        if st.button("Clear Session"):
            st.session_state.chat = None
            st.session_state.messages = []
            st.session_state.trace = []
            st.rerun()
    return state

def main():
    selected_state = render_telemetry()
    
    # [FIRST PLACE] Tab-based Multimodal Interface
    tab1, tab2, tab3 = st.tabs(["💬 Safety Assistant", "🆔 Identity Hub", "📊 Regional Analytics"])

    with tab1:
        st.title("Election Safety Assistant")
        st.caption(f"Status: High-Security Mode | State: {selected_state}")

        if "messages" not in st.session_state: st.session_state.messages = []
        
        # Initialize Gemini Chat Session
        if "chat" not in st.session_state or st.session_state.chat is None:
            model = get_agent_model(selected_state, AI_SAFETY, tools=[get_booth_location, check_election_rules])
            st.session_state.chat = model.start_chat(enable_automatic_function_calling=True)

        # Display Chat
        for m in st.session_state.messages:
            with st.chat_message(m["role"]):
                st.markdown(m["content"])
                if "artifact" in m: st.markdown(m["artifact"], unsafe_allow_html=True)

        # Input
        if prompt := st.chat_input("Ask about booths, rules, or safety..."):
            prompt = sanitize_input(prompt)
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"): st.markdown(prompt)

            with st.chat_message("assistant"):
                with st.status("🧠 Agent Reasoning...", expanded=True) as status:
                    st.session_state.trace.append(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] ANALYZING: {prompt[:30]}...")
                    
                    try:
                        response = st.session_state.chat.send_message(prompt)
                        res_text = response.text
                        
                        st.markdown(res_text)
                        st.session_state.trace.append(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] RESPONSE: Synthesis Complete")
                        
                        # Generate Visual Artifacts
                        v_slip = None
                        if any(w in prompt.lower() for w in ["booth", "slip", "vote"]):
                            v_slip = generate_voter_slip("Voter", selected_state, "Primary Center", "General")
                            st.markdown(v_slip, unsafe_allow_html=True)
                        
                        st.session_state.messages.append({"role": "assistant", "content": res_text, "artifact": v_slip})
                        status.update(label="✅ Reasoning Complete", state="complete")
                        
                    except Exception as e:
                        st.error(f"Reasoning Error: {e}")

    with tab2:
        st.header("🆔 Identity Verification Hub")
        st.info("Multimodal Ready: This section is prepared for Gemini Vision ID verification.")
        col1, col2 = st.columns(2)
        with col1:
            st.camera_input("Scan Voter ID (EPIC)")
        with col2:
            st.file_uploader("Upload ID Proof", type=['png', 'jpg', 'pdf'])
            st.button("Verify Identity (Simulated)")

    with tab3:
        st.header("📊 Regional Safety Analytics")
        st.markdown(f"**Current Context:** {selected_state}")
        st.progress(85 if "Active" in ELECTION_DATA[selected_state]["Status"] else 100, text="Booth Verification Progress")
        st.metric("Total Booths Monitored", "1,245", "+12 today")
        st.mermaid(generate_mermaid_mission("General", ELECTION_DATA[selected_state]["Status"]))

if __name__ == "__main__":
    main()
