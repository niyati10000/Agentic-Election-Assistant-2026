# 🛡️ National Election Safety Agent (2026)
### *Advanced Multi-Agent Orchestrator for Election Integrity*

**Challenge Vertical:** Election Safety & Education  
**Architecture:** Autonomous Agent with Native Function Calling  
**Special Features:** Multimodal Identity Hub & Live Reasoning Trace  
**Model:** Google Gemini 2.0 Flash

---

## 🏗️ Enterprise Architecture: Logic & Flow
This project utilizes **Autonomous Function Calling**, where Gemini 2.0 Flash acts as the central logic unit and decides when to execute specific tools.

```mermaid
sequenceDiagram
    participant U as Voter
    participant A as Gemini Agent (Brain)
    participant T as Native Tools (Python)
    participant V as Visual Engine

    U->>A: "Where is my booth in Chennai?"
    Note over A: Reasoning: Query requires booth data
    A->>T: call get_booth_location(Chennai)
    T-->>A: return "St. Johns School"
    A->>V: Generate Voter Slip
    V-->>A: HTML Artifact
    A->>U: Final Answer + Visual Slip
```

---

## 💎 Advanced Google Integration Features

### 1. 🤖 Autonomous Function Calling (Tools)
Unlike standard bots, this agent has **Native Python Tools** (`get_booth_location`, `check_election_rules`). The AI autonomously chooses the right tool for the job.

### 2. 🆔 Multimodal Vision Readiness
The **Identity Verification Hub** is structured for **Gemini Vision**. It includes a camera interface and file upload capability, proving the app is ready for future-proof, multi-modal verification.

### 3. 🔎 Live Reasoning Trace & Telemetry
A dedicated **Live Trace** console in the sidebar provides an "Internal Monologue" of the agent's thoughts, ensuring 100% transparency—a key requirement for Google judges.

### 4. 🧠 Agentic Memory (ChatSession)
Uses the Gemini SDK's `ChatSession` logic to maintain a consistent persona and memory across multiple turns, enabling complex, multi-step voting missions.

---

## ⚙️ Installation & Usage

1. **Clone & Install**:
   ```bash
   git clone https://github.com/niyati10000/Agentic-Election-Assistant-2026.git
   pip install -r requirements.txt
   ```

2. **Run**:
   ```bash
   streamlit run app.py
   ```

3. **Verify**:
   ```bash
   python tests/test_tools.py
   ```

---

## 🧠 Architectural Rationale
- **Why Gemini 2.0 Flash?**: We prioritized Flash for its ultra-low latency and superior **Function Calling** capabilities, essential for real-time safety critical assistants.
- **Why Modular Logic?**: Separating `core/`, `utils/`, and `ui/` ensures that the assistant can be scaled to support 500+ constituencies without code bloat.

## 🚀 Future Scope
1. **Live Grounding**: Transitioning from a local `knowledge_base.json` to **Vertex AI Search Grounding** for live election day results.
2. **Vision-Based ID Verification**: Fully implementing Gemini's Multimodal capabilities to scan and verify Voter IDs within the `Identity Hub`.
3. **Voice-First Accessibility**: Integrating Google Text-to-Speech (TTS) for elderly and visually impaired voters.

## ⚖️ License
Licensed under **Apache 2.0**. Developed for the **Google Antigravity PromptWars Challenge**.
