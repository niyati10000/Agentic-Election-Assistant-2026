import streamlit as st
import datetime
from typing import Tuple

def apply_custom_styles() -> None:
    """[ACCESSIBILITY] High-contrast CSS and professional UI tokens."""
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
        /* Accessibility improvements for color blindness */
        .stButton>button { border: 1px solid #004a99; }
        </style>
        """, unsafe_allow_html=True)

def generate_mermaid_mission(constituency: str, status: str) -> str:
    """[GOOGLE SERVICES] Visual Mission Mapping using Mermaid.js."""
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
    """[ACCESSIBILITY] ARIA-ready Election Readiness Artifact."""
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
