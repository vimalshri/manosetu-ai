import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage

st.set_page_config(page_title="ManoSetu AI", page_icon="🧘")
st.title("🧘 ManoSetu AI")
st.caption("A culturally intelligent companion for all students.")

# 1. API Key Setup
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=api_key)
except:
    st.error("API Key not found. Please add GOOGLE_API_KEY in Streamlit Advanced Settings.")
    st.stop()

# 2. Chat History
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Namaste! I am ManoSetu. How can I help you today?"}]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 3. Smart Response Logic
if prompt := st.chat_input("How are you feeling?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # ROUTER: Identify the problem category
        router_prompt = f"Categorize into ONE word: ACADEMIC, SOCIAL, REGULATORY, or SECURITY. Problem: {prompt}"
        category = llm.invoke(router_prompt).content.strip().upper()

        # MAPPING: Match to Mythology
        mapping = {
            "ACADEMIC": "Gita (Nishkama Karma) - Effort over marks.",
            "SOCIAL": "Hanuman - Inner strength vs comparison.",
            "REGULATORY": "Samudra Manthan - Struggle & need for rest.",
            "SECURITY": "Sudama & Krishna - Character value over wealth."
        }
        context = mapping.get(category, "General empathy.")

        # GENERATE: Create unique response
        response = llm.invoke(f"As ManoSetu AI, help this student using {context}: {prompt}").content
        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
