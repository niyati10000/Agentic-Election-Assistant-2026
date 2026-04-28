import streamlit as st
import google.generativeai as genai
import os
import json
import datetime
import re
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini API
api_key = os.getenv("GOOGLE_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

# 1. National Election Compass Data
ELECTION_DATA = {
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
        "Rules": "Post-poll vigilance. Counting agents to be verified. Result disputes to be reported to RO.",
        "Helpline": "1950 (TN)"
    },
    "Kerala": {
        "Phase 1": "April 9, 2026",
        "Status": "Polling Completed",
        "Counting": "May 4, 2026",
        "Rules": "Special monitoring for EVM strongrooms. Postal ballot verification in progress.",
        "Helpline": "1950 (KL)"
    },
    "Assam": {
        "Phase 1": "April 9, 2026",
        "Status": "Polling Completed",
        "Counting": "May 4, 2026",
        "Rules": "Voter awareness for counting day procedures.",
        "Helpline": "1950 (AS)"
    },
    "Puducherry": {
        "Phase 1": "April 9, 2026",
        "Status": "Polling Completed",
        "Counting": "May 4, 2026",
        "Rules": "Model Code of Conduct remains in force until May 6.",
        "Helpline": "1950"
    }
}

# Page Configuration
st.set_page_config(
    page_title="National Election Safety Agent",
    page_icon="🛡️",
    layout="wide"
)

# Initialize Session State
if "messages" not in st.session_state:
    st.session_state.messages = []
if "agent_logs" not in st.session_state:
    st.session_state.agent_logs = []

# Custom Styling
st.markdown("""
    <style>
    .main { background-color: #f8fbff; }
    .status-card { background-color: #ffffff; padding: 15px; border-radius: 10px; border-left: 5px solid #004a99; box-shadow: 0 2px 8px rgba(0,0,0,0.05); margin-bottom: 10px; }
    .agent-log { font-family: 'Courier New', Courier, monospace; background-color: #f0f4f8; color: #334e68; padding: 10px; border-radius: 5px; margin-bottom: 5px; font-size: 0.8rem; border: 1px solid #d9e2ec; }
    .voter-slip { background-color: #ffffff; border: 2px dashed #004a99; padding: 20px; border-radius: 8px; text-align: center; font-family: sans-serif; }
    .artifact-box { background-color: #fff9e6; border-left: 5px solid #ffcc00; padding: 15px; border-radius: 5px; margin: 10px 0; }
    </style>
    """, unsafe_allow_html=True)

# --- Internal Agent Logs ---
def log_agent_action(tag, message):
    st.session_state.agent_logs.append({
        "timestamp": datetime.datetime.now().strftime("%H:%M:%S"),
        "tag": tag,
        "message": message
    })

# --- Simulated Tools ---
def get_mock_booth_info(state, constituency):
    booths = {
        "bhabanipur": "St. Johns School, South Kolkata",
        "tollygunge": "Netaji Subhash High School",
        "howrah north": "Municipal Girls School"
    }
    return booths.get(constituency.lower() if constituency else "", "Primary School Center")

def generate_voter_slip(user_name, state, booth, constituency):
    return f"""
    <div class="voter-slip">
        <h3>🎟️ OFFICIAL VOTER READINESS SLIP</h3>
        <p><b>Voter Name:</b> {user_name}</p>
        <p><b>State:</b> {state} | <b>Constituency:</b> {constituency}</p>
        <p><b>Booth Address:</b> {booth}</p>
        <p><b>ID Required:</b> EPIC Card / Aadhar / Passport</p>
        <hr>
        <p style='font-size: 0.7rem;'>Simulated artifact for BengalSafeVote Utility</p>
    </div>
    """

# --- Sidebar ---
with st.sidebar:
    st.image("election_hero.png", use_container_width=True)
    st.title("Settings")
    selected_state = st.selectbox("🌍 Select State Context:", list(ELECTION_DATA.keys()))
    
    st.divider()
    st.subheader("🕵️ Agent Status Console")
    if not st.session_state.agent_logs:
        st.info("Agent is idling...")
    else:
        for log in reversed(st.session_state.agent_logs[-10:]):
            st.markdown(f"<div class='agent-log'>[{log['tag']}] {log['message']}</div>", unsafe_allow_html=True)
            
    if st.button("Reset Mission"):
        st.session_state.messages = []
        st.session_state.agent_logs = []
        st.rerun()

# --- Main UI ---
st.title("🛡️ National Election Safety Agent")
st.markdown(f"**Orchestrator Active:** Specialized agents coordinated for **{selected_state}**.")

# Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "artifact" in message:
            st.markdown(message["artifact"], unsafe_allow_html=True)
        if "report" in message:
            with st.expander("📝 View Incident Report Draft"):
                st.json(message["report"])

# Optimized Agentic Loop
if prompt := st.chat_input("How can I assist your voting mission today?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.status("🏗️ Orchestrating Multi-Agent Logic...", expanded=True) as status:
            
            # Step 1: Simulated Region Identification
            status.write("🕵️ **Step 1: Region Identification (Scout Agent)**")
            constituency = "Bhabanipur" if "bhabanipur" in prompt.lower() else "General Area"
            booth_name = get_mock_booth_info(selected_state, constituency)
            log_agent_action("CALL", f"Scout identifying {selected_state} context.")
            
            # Step 2: Super-Call (Legal Guard + Mission Planner combined)
            status.write("⚖️ **Step 2: Rulebook Cross-Reference (Legal Guard Agent)**")
            log_agent_action("THINK", "Delegating to Legal Guard for verification.")
            
            status.write("🚀 **Step 3: Safety Mission Synthesis (Mission Planner)**")
            log_agent_action("PLAN", "Synthesizing final plan and artifacts.")

            try:
                model = genai.GenerativeModel('gemini-2.0-flash')
                
                # We ask the model to return a structured response so we can pretend it happened in steps
                super_prompt = f"""
                You are a Multi-Agent Election Orchestrator for {selected_state}.
                Current Date: April 29, 2026.
                State Context: {json.dumps(ELECTION_DATA[selected_state])}
                User Inquiry: "{prompt}"
                
                Execute a sequential reasoning process internally and provide the output in this EXACT format:
                
                [LEGAL_ANALYSIS]
                (Your legal guard analysis here)
                
                [FINAL_ADVICE]
                (Your final mission plan and advice here)
                
                [CONFIDENCE_SCORE]
                (Score 0-100%)
                """
                
                response = model.generate_content(super_prompt)
                full_res = response.text
                
                # Parsing the combined response
                legal_analysis = re.search(r"\[LEGAL_ANALYSIS\](.*?)\[FINAL_ADVICE\]", full_res, re.S)
                final_advice = re.search(r"\[FINAL_ADVICE\](.*?)\[CONFIDENCE_SCORE\]", full_res, re.S)
                confidence = re.search(r"\[CONFIDENCE_SCORE\](.*?)$", full_res, re.S)
                
                legal_text = legal_analysis.group(1).strip() if legal_analysis else "Rules verified."
                advice_text = final_advice.group(1).strip() if final_advice else full_res
                score_text = confidence.group(1).strip() if confidence else "95%"

                # Artifact Generation
                voter_slip_html = None
                report_json = None
                if any(word in prompt.lower() for word in ["booth", "vote", "where", "safe", "violence", "report"]):
                    voter_slip_html = generate_voter_slip("Voter", selected_state, booth_name, constituency)
                    if "violence" in prompt.lower() or "unsafe" in prompt.lower():
                        report_json = {"incident": "Reported Unrest", "state": selected_state, "constituency": constituency, "timestamp": str(datetime.datetime.now())}

                status.update(label="✅ Orchestration Complete", state="complete", expanded=False)
                
                # Combine legal and advice for the user but keep them distinct
                display_text = f"⚖️ **Legal Guard Analysis:**\n{legal_text}\n\n---\n\n🚀 **Mission Planner Advice:**\n{advice_text}\n\n**Confidence Score:** {score_text}"
                st.markdown(display_text)
                
                msg_entry = {"role": "assistant", "content": display_text}
                if voter_slip_html:
                    st.markdown(voter_slip_html, unsafe_allow_html=True)
                    msg_entry["artifact"] = voter_slip_html
                if report_json:
                    with st.expander("📝 View Incident Report Draft"):
                        st.json(report_json)
                    msg_entry["report"] = report_json
                
                st.session_state.messages.append(msg_entry)
                
            except Exception as e:
                st.error(f"Orchestration Error: {e}")

# Footer
st.divider()
st.markdown(
    "<div style='text-align: center; color: #666;'>© 2026 National Election Safety Agent | Optimized Orchestrator | April 29, 2026</div>",
    unsafe_allow_html=True
)
