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
    # Show user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate Response
    with st.chat_message("assistant"):
        # STEP A: THE EMOTION ROUTER
        # We ask Gemini to categorize the student's problem first
        router_prompt = f"""
        Analyze this student's message: "{prompt}"
        Classify it into exactly one of these 4 categories:
        1. ACADEMIC (Exams, Results, Study pressure)
        2. SOCIAL (Peer pressure, Parents, Loneliness, Comparison)
        3. REGULATORY (Burnout, Sleep issues, Brain fog, Exhaustion)
        4. SECURITY (Money, Loans, Placement, Career fear, Future stability)
        Respond with ONLY the category name.
        """
        
        try:
            category_result = llm.invoke(router_prompt).content.strip().upper()
            
            # STEP B: ASSIGN MYTHOLOGICAL CONTEXT
            if "SECURITY" in category_result:
                myth_context = "Talk about Sudama and Krishna. Emphasize that worth is not wealth, and character brings sustenance."
            elif "ACADEMIC" in category_result:
                myth_context = "Use the Bhagavad Gita's 'Nishkama Karma'. Focus on the effort, not the exam result."
            elif "SOCIAL" in category_result:
                myth_context = "Mention Hanuman and Jamvant. Remind them of their inner strength that is often hidden by comparison."
            elif "REGULATORY" in category_result:
                myth_context = "Refer to the Samudra Manthan. Explain that rest is needed when the 'churning' of life gets intense."
            else:
                myth_context = "Provide general empathetic mythological guidance."

            # STEP C: GENERATE FINAL RESPONSE
            final_messages = [
                SystemMessage(content=system_prompt + f"\nSpecific Context for this session: {myth_context}"),
                HumanMessage(content=prompt)
            ]
            
            response = llm.invoke(final_messages)
            full_response = response.content
            
            # Optional: Display the recognized category to the student
            st.caption(f"Topic: {category_result}")
            st.markdown(full_response)
            
        except Exception as e:
            st.error("Something went wrong with the AI brain. Please try again.")
            full_response = "I am here for you, but I'm having trouble connecting right now."

    st.session_state.messages.append({"role": "assistant", "content": full_response})
