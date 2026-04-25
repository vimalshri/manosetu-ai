import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage

# 1. Page Config
st.set_page_config(page_title="ManoSetu AI", page_icon="🧘")
st.title("🧘 ManoSetu AI")
st.caption("A culturally intelligent companion for all students.")

# 2. API Key Setup
try:
    api_key = st.secrets["AIzaSyBSdFw4waIgS5OI9HsdtYzgBu-RPImZubs"]
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=api_key)
except:
    st.error("API Key not found. Please add GOOGLE_API_KEY in Streamlit Secrets.")
    st.stop()

# 3. Chat History
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Namaste! I am ManoSetu. I am here to listen to your journey. What is on your mind?"}]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 4. Response Logic
if prompt := st.chat_input("How are you feeling?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # A: Classify the emotion
            router_text = f"Categorize this student problem into one word: ACADEMIC, SOCIAL, REGULATORY, or SECURITY. Problem: {prompt}"
            # Wrapping the input in a list of messages for stability
            category_resp = llm.invoke([HumanMessage(content=router_text)])
            category = category_resp.content.strip().upper()

            # B: Map to Mythology
            mapping = {
                "ACADEMIC": "Bhagavad Gita (Focus on effort, not results).",
                "SOCIAL": "Ramayana (Finding inner strength like Hanuman).",
                "REGULATORY": "Samudra Manthan (Patience during the struggle).",
                "SECURITY": "Sudama & Krishna (Character is true wealth)."
            }
            context = mapping.get(category, "General mythological empathy.")

            # C: Final Response
            final_query = f"As ManoSetu AI, an empathetic mental health chatbot, use the story of {context} to help a student who said: {prompt}"
            response = llm.invoke([HumanMessage(content=final_query)]).content
            
            st.caption(f"Context: {category}")
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

        except Exception as e:
            st.error("Connection Error. Please check your API key in Streamlit Secrets.")
