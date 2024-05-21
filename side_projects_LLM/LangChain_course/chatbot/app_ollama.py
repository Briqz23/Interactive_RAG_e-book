from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate 
from langchain_core.output_parsers import StrOutputParser
from langchain_community.llms import Ollama


import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()

os.environ['LANGCHAIN_TRACING_V2'] = 'true'
os.environ['LANGCHAIN_API_KEY'] = os.getenv('LANGCHAIN_API_KEY', 'nao encontrada')

prompt = ChatPromptTemplate.from_messages(
    [
        
        ("system", "you are a cat called little pattern. You miss YUN, but especially her food. YUN is also a cat, but your owner, she is a cute fluffy cat. You miss the naps at her bed!"),
       
         
        ("user", "Question:{question}")

    ])

#streamlit
st.title("Chat with the a cool eindhoven cat.")
input_text = st.text_input("Talk to him!")


#puxando llm
llm = Ollama(model="gemma:2b")
output_parser = StrOutputParser()
chain=prompt|llm|output_parser
#https://github.com/ollama/ollama --> llms que ele roda


if input_text:
    st.write(chain.invoke({"question": input_text}))  