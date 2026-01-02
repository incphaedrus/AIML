# -----------------------------------------------
# Example Cha application using LLM model, UI via streamlit
# Ensure  API keys are added in .env
# To invoke run--> streamlit run chat_app.py
# -----------------------------------------------
import streamlit as st
import openai
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate


import os
from dotenv import load_dotenv
load_dotenv()

#os.environ["OLLAMA_API_KEY"] = os.getenv("OLLAMA_API_KEY")  
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGSMITH_API_KEY"] = os.getenv("LANGSMITH_API_KEY")
os.environ["LANGCHAIN_PROJECT"] = "chat_app_project"
 



## prompt template
prompt = ChatPromptTemplate.from_messages(
  [
    ("system", "you are a helpful assistant. Please respond to the user queries as best as you can."),
    ("user", "Question:{question}"),
  ]
)

### function to generate response based on question and llm model
def generate_response(question,api_key,llm, temperature, max_tokens):
    openai.api_key = api_key
    llm = ChatOpenAI(model_name=llm)
    output_parser = StrOutputParser()
    chain = prompt | llm | output_parser
    answer = chain.invoke({"question": question})   
    return answer 

 ## Streamlit app
 ## --------------------------------------------------------------------------------##
st.title("Chat Application with LLMs")  
api_key = st.text_input("Enter your OpenAI API Key:", type="password")

## createa a dropdown to select llm model
llm = st.selectbox("Select LLM Model:", ["gpt-3.5-turbo", "gpt-4", "gpt-4o"])

temperature = st.slider("Select Temperature:", 0.0, 1.0, 0.5)
max_tokens = st.slider("Select Max Tokens:", 50, 300, 100)

st.write("## Enter your question below:")
user_input = st.text_area("Your Question:")

if user_input:
    response=generate_response(user_input, api_key, llm, temperature, max_tokens)
    st.write("## Response:")
    st.write(response)
else:
    st.write("No question entered yet.")
     
