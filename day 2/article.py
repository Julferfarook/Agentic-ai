import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import Runnable

# 🔐 Set your Gemini API key directly here (not secure for production)
GOOGLE_API_KEY = "AIzaSyCsINRQVql0DWC3uZiWmA47ZLwS-EGkdPE"  # Replace with your actual Gemini API key

# Initialize Gemini model via LangChain
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0.7,
    google_api_key=GOOGLE_API_KEY
)

# 🧠 Define a prompt to generate an article
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant that writes clear and informative articles on any topic."),
    ("user", "Write a detailed article about the following topic:\n\n{input}")
])

# 🔗 Create the chain using the prompt and LLM
chain: Runnable = prompt | llm

# 🎨 Streamlit UI
st.set_page_config(page_title="📝 Article Generator", page_icon="📝")
st.title("📝 AI Article Generator")
st.markdown("Enter a topic or sentence and generate a full article using Google Gemini.")

# Text input
user_input = st.text_input("Enter a topic or sentence:")

# Generate button
if st.button("Generate Article"):
    if not user_input.strip():
        st.warning("⚠️ Please enter a topic or sentence to generate an article.")
    else:
        try:
            # Invoke the chain
            response = chain.invoke({"input": user_input})
            # Display result
            st.success("✅ Article generated successfully!")
            st.markdown("### 📰 Generated Article")
            st.markdown(response.content)
        except Exception as e:
            st.error(f"❌ An error occurred: {str(e)}")
