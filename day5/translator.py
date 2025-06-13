import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import Runnable

# 🔑 Set your Gemini API key directly here (NOT secure for production)
GOOGLE_API_KEY = "AIzaSyCsINRQVql0DWC3uZiWmA47ZLwS-EGkdPE"  # Replace with your actual API key

# Initialize Gemini model using LangChain
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0.3,
    google_api_key=GOOGLE_API_KEY
)

# 🧠 Define the prompt using LangChain's ChatPromptTemplate
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant that translates English sentences into French."),
    ("user", "Translate this sentence to French:\n\n{input}")
])

# 🔗 Create the chain using prompt | llm
chain: Runnable = prompt | llm

# 🎨 Streamlit UI
st.set_page_config(page_title="English to French Translator", page_icon="🌐")
st.title("🌐 English to French Translator")

# Text input
user_input = st.text_input("Enter an English sentence:")

# Translate button
if st.button("Translate"):
    if not user_input.strip():
        st.warning("Please enter a sentence before translating.")
    else:
        try:
            # Run the chain with input
            response = chain.invoke({"input": user_input})
            # Display translation
            st.success("✅ Translation successful!")
            st.markdown(f"**French Translation:**\n\n> {response.content}")
        except Exception as e:
            st.error(f"❌ An error occurred: {str(e)}")
