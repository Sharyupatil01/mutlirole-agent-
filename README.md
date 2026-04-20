# 🤖 Multi-Role AI Agent (ReAct Framework)

A professional AI Agent built using Python, Streamlit, and Ollama. This project implements the ReAct (Reason + Act) framework, enabling the agent to not only respond to queries but also take actions using tools to generate accurate, grounded answers.

---
## 📷 Screenshots

<p align="center">
  <img src="https://github.com/user-attachments/assets/10d77d88-b5a7-440a-9172-decf11adc882" width="30%" />
  <img src="https://github.com/user-attachments/assets/0c74f675-db3c-4223-abae-29f4568fe90f" width="30%" />
  <img src="https://github.com/user-attachments/assets/78b555a7-f1f7-4a9d-9e70-0d6023ff8206" width="30%" />
</p>

![Watch Demo](https://github.com/user-attachments/assets/0956fdb9-9784-401d-b520-fdc32221424e)






## 🚀 Overview

Unlike traditional chatbots, this Multi-Role AI Agent goes beyond conversation—it performs actions. When it encounters queries requiring real-time data or computation, it follows a structured reasoning loop:

- **Thought** → Understands and analyzes the query
- **Action** → Selects an appropriate tool
- **Observation** → Retrieves tool output
- **Final Answer** → Produces a grounded and reliable response

This loop ensures reduced hallucination and improved accuracy.

---

## 🛠️ Features

- **Parallel Tool Calling**: Handles multiple tool requests in a single query (e.g., weather in multiple cities)
- **Self-Correction Mechanism**: Detects and corrects hallucinated responses using tool outputs
- **Interactive UI**: Built with Streamlit for a smooth and user-friendly interface
- **Local & Private Execution**: Runs entirely on your system using LLaMA 3 via Ollama

---

## 🧰 Integrated Tools

### 🔢 Calculator
- Evaluates arithmetic expressions
- Handles nested operations and precedence

### 🌦️ Weather Tool (Mock)
- Provides temperature and weather conditions
- Demonstrates grounding using external tools

---

## 🏗️ Technical Architecture

The system follows the ReAct pattern with a custom orchestration layer:

- **System Prompting**: Forces structured outputs like `CALL: tool_name(args)`
- **Regex Parsing**: Uses `re.finditer` to detect multiple tool calls
- **Context Injection**: Feeds tool outputs back as observations for better reasoning

---

## 📋 Requirements

- Python 3.10+
- Ollama (with llama3 installed)
- requests
- streamlit

---

## ⚙️ Setup & Installation

### 1. Clone the Repository
```bash
git clone https://github.com/Sharyupatil01/mutlirole-agent-.git
cd mutlirole-agent-
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Download llama3 
```bash
ollama pull llama3
```

### 4. Run Ollama
```bash
ollama run llama3
```

### 4. Start the App (Another Terminal)
```bash
streamlit run app.py
```

---

## 🧠 Lessons Learned

- **Prompt Engineering**: Reduced hallucinations using strict reasoning constraints
- **Regex Optimization**: Handled complex tool-call parsing with greedy matching
- **State Management**: Maintained conversation memory using Streamlit session_state

---

