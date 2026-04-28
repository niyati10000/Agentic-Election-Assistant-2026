# 🛡️ National Election Safety Agent (2026)

### *A Multi-Agent Orchestrator for Secure and Informed Voting*

The **National Election Safety Agent** is a sophisticated AI-driven assistant designed to empower voters during the 2026 Indian General Elections. Unlike basic chatbots, this system utilizes a **Multi-Agent Orchestrator** architecture and the **ReAct (Reasoning and Acting)** pattern to provide localized safety missions, rulebook verification, and actionable voting utilities.

---

## 🚀 Key Features

### 🤖 Multi-Agent Orchestration
The system coordinates three specialized internal agents to ensure accuracy and safety:
- **🕵️ Scout Agent**: Fetches real-time, state-specific polling data, phases, and booth locations.
- **⚖️ Legal Guard Agent**: A "read-only" reasoning block that verifies claims and rumors against the **ECI 2026 Rulebook**.
- **🚀 Mission Planner (Lead Agent)**: Synthesizes data into a personalized "Action Plan" for the voter.

### 🌍 National Election Compass
Seamlessly switch between multiple polling states (West Bengal, Tamil Nadu, Kerala, Assam, Puducherry). The agent dynamically pivots its knowledge base:
- **Active Mode**: Focuses on live polling safety (e.g., West Bengal Phase 2).
- **Vigilance Mode**: Focuses on post-poll monitoring and counting prep (e.g., Tamil Nadu).

### 🔍 Transparency & Tool Logs
Built for total transparency, the **Agent Status Console** logs every internal `[THINK]`, `[CALL]`, and `[PLAN]` step, allowing users and judges to see exactly how the AI reached its conclusions.

### 🛠️ Actionable Artifacts
The agent generates functional utilities beyond simple text:
- **🎟️ Provisional Voter Slip**: A personalized template with booth details and required IDs.
- **📝 Incident Report Draft**: A pre-formatted JSON block for direct reporting of violations (e.g., to cVIGIL or Voter Helpline).

---

## 🛠️ Tech Stack

- **Frontend**: [Streamlit](https://streamlit.io/)
- **AI Brain**: [Google Gemini 2.0 Flash](https://aistudio.google.com/)
- **Logic**: Python (Multi-Agent Orchestration Logic)
- **Environment**: `python-dotenv` for secure API management.

---

## ⚙️ Installation & Setup

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/niyati10000/Agentic-Election-Assistant-2026.git
   cd Agentic-Election-Assistant-2026
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment Variables**:
   Create a `.env` file in the root directory and add your Google Gemini API Key:
   ```env
   GOOGLE_API_KEY=your_gemini_api_key_here
   ```

4. **Run the Application**:
   ```bash
   streamlit run app.py
   ```

---

## 💎 Technical Merit & Evaluation Focus

This solution was engineered to excel in the following areas:

### 1. Code Quality & Maintainability
- **Modular Design**: Separated UI logic, agent tools, and data models.
- **Type Safety**: Fully implemented Python Type Hints for robust development.
- **Documentation**: Professional docstrings and internal logging for every agent action.

### 2. Security & Responsibility
- **Environment Management**: Secure API key handling via `python-dotenv` and `.gitignore`.
- **Error Handling**: Implemented robust exception handling for API failures and missing keys.

### 3. Efficiency
- **Orchestration Optimization**: Uses a single-call orchestration pattern to minimize API quota consumption while maintaining a multi-agent user experience.

### 4. Testing & Validation
- **Unit Testing**: Includes a `tests/` suite (powered by `unittest`) to validate the accuracy of the Scout Agent and Election Compass data.

### 5. Accessibility
- **Inclusive Design**: Added ARIA labels, descriptive help text for UI elements, and a high-contrast theme for better usability.

### 6. Google Services Integration
- **Gemini 2.0 Flash**: Leverages the high-speed reasoning of Gemini 2.0 to power the "Inner Monologue" and ReAct loop.

---

## 📋 Example Interactions

- **Query**: *"Where is my booth in Bhabanipur and is it safe today?"*
- **Agent Action**: The Scout locates the booth, the Legal Guard checks the Phase 2 rules, and the Planner generates a safety mission and a voter slip.

- **Query**: *"I heard voting in Chennai is extended to 8 PM."*
- **Agent Action**: The Legal Guard cross-references the rulebook and debunks the rumor based on the official 6 PM deadline.

---

## ⚖️ Disclaimer
This project is an AI-driven simulation developed for the **PromptWars/Google Solution Challenge**. All data, including booth locations and incident reports, are for demonstration purposes and should be verified with the **Election Commission of India (ECI)** official portal.

---
*Created with ❤️ for a safer democracy in 2026.*
