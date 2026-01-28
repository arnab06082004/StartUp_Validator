# Brutal Startup Idea Validator 💡

A professional, AI-powered tool for evaluating startup ideas with structured, context-aware analysis. The application identifies whether the input represents a new startup concept or a follow-up inquiry, then generates investment, market, revenue, and risk insights with adjustable critique intensity.

---

## Key Features

- **Intelligent Input Classification**  
  Distinguishes between new startup ideas and continuation questions.

- **Context-Aware Follow-ups**  
  Maintains ongoing conversation context for deeper exploration.

- **Structured Startup Evaluation**  
  Includes:
  - Idea feasibility
  - Market potential
  - Investment requirements
  - Unit economics & burn rate
  - Risk factors & failure scenarios
  - Revenue and exit possibilities

- **Adjustable Brutality Level (1–10)**  
  Controls the level of critique and directness.

- **Streamed Chat Experience**  
  ChatGPT-like interface with real-time LLM token streaming.

- **Optional Business Context Fields**  
  Target market, budget range, and execution timeline.

---

## Tech Stack

- **Frontend:** Streamlit
- **LLM Pipeline:** LangChain
- **LLM Provider:** Groq (Llama 3.3 70B Versatile)
- **Environment Handling:** python-dotenv
- **Language:** Python 3.10+

---

## Application Overview

The tool operates in two stages:

1. **Validation Stage**  
   Uses a deterministic prompt-driven model to classify input as:
   - `STARTUP` (new idea)
   - `OTHER` (follow-up query or generic message)

2. **Analysis Stage**  
   Performs detailed breakdown based on:
   - Investment
   - Market
   - Risks
   - Profitability
   - Scalability
   - Strategic roadmap

Session state is used to preserve conversation continuity across exchanges.

---

## Installation

Clone the repository:

```bash
git clone https://github.com/arnab06082004/StartUp_Validator.git
cd startup-validator
