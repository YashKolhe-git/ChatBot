import streamlit as st
import openai
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate


import os
from dotenv import load_dotenv

import os
from dotenv import load_dotenv


load_dotenv()


api_key = os.getenv("LANGCHAIN_API_KEY")


os.environ['LANGCHAIN_API_KEY'] = api_key
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = os.getenv("LANGCHAIN_PROJECT", "Default Project")



prompt = ChatPromptTemplate.from_messages(
    [
    ("system", "you are a helpful assistant. Please response to the given user query"),
    ("user", "Question: {question}")
    ]
)


def generate_response(question, api_key, engine, temperature, max_tokens):

    openai.api_key = api_key
    llm = ChatOpenAI(model=engine, openai_api_key=api_key)
    output_parser = StrOutputParser()
    chain = prompt|llm|output_parser
    answer = chain.invoke({"question":question})
    return answer




#title of the app
st.title("QNA Chatbot With OpenAI")


##sidebar for setting
st.sidebar.title("Setting")
api_key = st.sidebar.text_input("Enter your Open AI API key", type="password")


#dropdown to select various OPENAI model

engine = st.sidebar.selectbox("Select an Open AI model", ["gpt-4o", "gpt-4-turbo", "gpt-4"])



#slider for Temperature

temperature = st.sidebar.slider("Temperature", min_value=0.0, max_value=1.0,value=0.7)

max_tokens = st.sidebar.slider("Max Tokens", min_value=50, max_value = 300, value=150)



#Main interface for user input

st.write("Go ahead and ask any question")
user_input = st.text_input("you: ")

if user_input:
    response = generate_response(user_input, api_key, engine , temperature, max_tokens)
    st.write(response)

else:
    st.write("Please provide the question")
