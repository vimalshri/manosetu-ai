import streamlit as st
import random

# 1. Page Configuration
st.set_page_config(page_title="ManoSetu AI", page_icon="🧘")
st.title("🧘 ManoSetu AI: Student Support")
st.markdown("---")

# 2. Initialize Chat History (Memory)
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Namaste! I am ManoSetu. I'm here to support you through your MTech journey. How are you feeling today?"}
    ]

# 3. Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. Chat Input
if prompt := st.chat_input("Tell me what's on your mind..."):
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 5. The Response Logic (Connecting to your RAG/Gemini)
    # For now, we simulate a response
    with st.chat_message("assistant"):
        response = "I hear you. Remember, 'Nishkama Karma'—focus on your effort, and let the results take care of themselves."
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})