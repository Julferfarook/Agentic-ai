import streamlit as st
from langchain.agents import initialize_agent, AgentType
from langchain.tools import DuckDuckGoSearchRun
from langchain_google_genai import ChatGoogleGenerativeAI

# 🔐 Hardcoded Gemini API key (NOT recommended for production)
GOOGLE_API_KEY = "AIzaSyCsINRQVql0DWC3uZiWmA47ZLwS-EGkdPE
"  # Replace with your actual Gemini API key

# 🌐 Initialize Gemini LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-pro",  # change from gemini-2.0-flash
    temperature=0.5,
    google_api_key=GOOGLE_API_KEY
)

# 🔎 Add DuckDuckGoSearch tool
search_tool = DuckDuckGoSearchRun()

# 🤖 Initialize the agent with search tool
agent = initialize_agent(
    tools=[search_tool],
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=False  # No terminal logging
)

# 🎨 Streamlit UI
st.set_page_config(page_title="🌐 Real-Time Q&A with Gemini", page_icon="🌍")
st.title("🌐 Ask Real-World Questions (Powered by Gemini + DuckDuckGo)")
st.markdown("Type a question about current events, recent news, or factual info, and get a real-time response.")

# Input field and button
user_question = st.text_input("❓ Enter your question here:")
if st.button("🔍 Get Answer"):
    if not user_question.strip():
        st.warning("⚠️ Please enter a question first.")
    else:
        try:
            with st.spinner("Thinking..."):
                answer = agent.run(user_question)
            st.success("✅ Answer retrieved successfully!")
            st.markdown("### 🧠 Gemini's Response:")
            st.write(answer)
        except Exception as e:
            st.error(f"❌ Something went wrong: {str(e)}")

# Footer
st.markdown("---")
st.caption("🔒 Powered by Google Gemini + DuckDuckGo · Built with LangChain + Streamlit")
