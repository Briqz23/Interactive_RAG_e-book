from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate 
from langchain_core.output_parsers import StrOutputParser

import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()

#langsmith tracker
os.environ['LANGCHAIN_TRACING_V2'] = 'true'
os.environ['LANGCHAIN_API_KEY'] = os.getenv('LANGCHAIN_API_KEY', 'nao encontrada')
os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY', 'nao encontraaada')

prompt = ChatPromptTemplate.from_messages(
    [
        
        ("system", "you are a cat called little pattern. All you say to others is meow and fuck off     "),
        ("user", "Question:{question}")

    ])

st.title("Chat with the a cat that has recently become a human.")
input_text = st.text_input("Talk to him!")

llm = ChatOpenAI(model="gpt-3.5-turbo")
output_parser = StrOutputParser()

chain=prompt|llm|output_parser

if input_text:
    st.write(chain.invoke({"question": input_text}))  