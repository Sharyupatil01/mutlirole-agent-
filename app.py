import streamlit as st
import requests
import re

# --- 1. THE TOOLS (Backend Logic) ---

def calculator(expression):
    try:
        # Basic cleaning of the string for eval
        clean_expr = expression.replace(" ", "").strip("'").strip('"')
        return str(eval(clean_expr))
    except Exception as e:
        return f"Error: {str(e)}"

def get_weather(city):
    # Cleaning the input (removing quotes/spaces LLMs often add)
    city = city.strip().strip("'").strip('"').lower()
    
    weather_data = {
        "pune": "30", # Simplified to numbers for easier math
        "mumbai": "35",
        "london": "15",
        "new york": "22"
    }
    return weather_data.get(city, "18")

# Tool registry
TOOLS = {
    "calculator": calculator,
    "get_weather": get_weather
}

# --- 2. THE BRAIN (Ollama Interaction) ---

def call_llm(messages):
    url = "http://localhost:11434/api/chat"
    try:
        response = requests.post(
            url,
            json={"model": "llama3", "messages": messages, "stream": False},
            timeout=30
        )
        response.raise_for_status()
        return response.json()["message"]["content"]
    except Exception as e:
        return f"Backend Connection Error: {str(e)}"

# --- 3. STREAMLIT UI ---

st.set_page_config(page_title="ReAct AI Agent", page_icon="🤖")
st.title("🤖 Multi-Tool AI Agent")
st.markdown("""
This agent uses the **ReAct (Reason + Act)** pattern to solve problems.
It can check the **weather** and perform **calculations** by calling local Python tools.
""")

# Initialize chat history (Session State)
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display previous messages
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
if user_query := st.chat_input("Ex: What is the weather in Pune and Mumbai added together?"):
    
    # 1. Display User Message
    st.chat_message("user").markdown(user_query)
    st.session_state.chat_history.append({"role": "user", "content": user_query})

    # 2. Start Agent Orchestration
    # Prepare the initial messages with the Strict System Instruction
    messages = [
        {
            "role": "system", 
            "content": """You are a precise AI Agent.
Available tools:
- calculator(expression): Use for math. Input: string like "10+5".
- get_weather(city): Use for temperature. Input: city name.

Rules:
1. Format for calling: CALL: tool_name(input)
2. You can call multiple tools at once.
3. DO NOT guess the answer. Use the tool results.
4. Once you have the results, give a natural final answer."""
        },
        {"role": "user", "content": user_query}
    ]

    with st.chat_message("assistant"):
        # We use a container to show "Thoughts" separately from the "Final Answer"
        thought_container = st.container()
        
        # Max 5 turn loop
        for step in range(5):
            with st.spinner(f"Agent thinking (Step {step+1})..."):
                response = call_llm(messages)
            
            # Display the LLM's thought process
            with thought_container:
                st.info(f"**Step {step+1} Thought:**\n{response}")

            # Check for tool calls
            tool_calls = list(re.finditer(r"CALL:\s*(\w+)\((.*)\)", response))

            if not tool_calls:
                # Final answer reached
                st.success("**Final Answer:**")
                st.markdown(response)
                st.session_state.chat_history.append({"role": "assistant", "content": response})
                break
            
            # If tools are called, execute them
            messages.append({"role": "assistant", "content": response})
            
            results = []
            for match in tool_calls:
                name, args = match.group(1), match.group(2)
                if name in TOOLS:
                    result = TOOLS[name](args)
                    st.toast(f"Executed {name}({args})")
                    results.append(f"Observation from {name}({args}): {result}")
                else:
                    results.append(f"Error: Tool '{name}' not found.")
            
            # Feed results back
            obs_text = "\n".join(results)
            messages.append({
                "role": "user", 
                "content": f"{obs_text}\nNow provide the final answer."
            })