import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage
import json
import os

# 1. Page Setup
st.set_page_config(page_title="ManoSetu AI", page_icon="🧘")
st.title("🧘 ManoSetu AI")
st.caption("A culturally intelligent companion for all students.")

# 2. Setup Gemini (Using the Secret Key you added to Streamlit)
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=api_key)
except Exception as e:
    st.error("API Key not found. Please add GOOGLE_API_KEY in Streamlit Advanced Settings.")
    st.stop()

# 3. Universal System Prompt
system_prompt = """
You are ManoSetu AI, an empathetic mental health companion for students of all levels (School, College, University).
Your goal is to help with exam stress, academic pressure, and general well-being.
Instructions:
1. Use Indian mythological stories (Gita, Ramayana, etc.) to offer perspective.
2. Be supportive and non-judgmental.
3. If a student mentions self-harm, immediately provide this helpline: Vandrevala Foundation (9999 666 555).
4. Do not mention specific degrees like MTech unless the student mentions it first.
"""

# 4. Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Namaste! I am ManoSetu. Whether you're in school, college, or preparing for exams, I am here for you. What's on your mind?"}
    ]

# 5. Display Messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 6. User Input & AI Response
if prompt := st.chat_input("How are you feeling?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # This part makes the AI 'think' instead of repeating
        router_prompt = f"Identify the emotion: ACADEMIC, SOCIAL, REGULATORY, or SECURITY. Text: {prompt}"
        category = llm.invoke(router_prompt).content.strip().upper()

        mapping = {
            "ACADEMIC": "Gita (Nishkama Karma) - Focus on effort.",
            "SOCIAL": "Hanuman - Inner strength.",
            "REGULATORY": "Samudra Manthan - Need for rest.",
            "SECURITY": "Sudama & Krishna - Values over money."
        }
        myth_context = mapping.get(category, "General empathy.")

        # This generates a NEW, unique response every time
        response = llm.invoke(f"As ManoSetu AI, help this student using {myth_context}: {prompt}").content
        
        st.caption(f"Mapped to: {category}")
        st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})
