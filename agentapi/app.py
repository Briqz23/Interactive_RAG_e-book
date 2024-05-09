import arxiv
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper

api_wrapper = WikipediaAPIWrapper(top_k_results=1,document_content_chars_max=200)   
wiki = WikipediaQueryRun(api_wrapper = api_wrapper)

from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from fastapi import FastAPI
from pydantic import BaseModel

loader = WebBaseLoader("https://aliceinwonderland.fandom.com/wiki/Alice")
docs = loader.load()
RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200).split_documents(docs)

vectordb = FAISS.from_documents(docs, OpenAIEmbeddings())



#pdf
from langchain_community.document_loaders import PyPDFLoader

loaderPDF = PyPDFLoader('alice_in_wonderland.pdf')
docsPDF = loaderPDF.load()


text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=200)
documents = text_splitter.split_documents(docsPDF)

db2 = FAISS.from_documents(documents[:20], OpenAIEmbeddings())

vectordb.merge_from(db2)

retriever = vectordb.as_retriever() #retriever is the interface that will retrieve the result from FAISS
retriever

#creating the retriever tool as in https://api.python.langchain.com/en/latest/tools/langchain.tools.retriever.create_retriever_tool.html

from langchain.tools.retriever import create_retriever_tool
retriever_tool = create_retriever_tool(retriever, "langsmith_search", "search about information regarding Alice in Wonderland. Try to trace a personality she might have met in the story.")
retriever_tool.name

##Arxiv Tool

from langchain_community.utilities import ArxivAPIWrapper
from langchain_community.tools import ArxivQueryRun

arxiv_wrapper = ArxivAPIWrapper(top_k_results=1,document_content_chars_max=200)
arxiv = ArxivQueryRun(arxiv_wrapper = arxiv_wrapper)

tools = [wiki, retriever_tool, arxiv] #if it doesnt get the info on tool, tru on retirever, then arxiv

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

os.environ['LANGCHAIN_TRACING_V2'] = 'true'
os.environ['LANGCHAIN_API_KEY'] = os.getenv('LANGCHAIN_API_KEY', 'nao encontrada')
os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY', 'nao encontraaada')

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)


#criando o prompt de uma forma diferente - pegando da comunidade

from langchain import hub
#https://smith.langchain.com/hub/rlm/rag-prompt
#prompt = hub.pull("hwchase17/openai-functions-agent")
#prompt.messages


from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate, MessagesPlaceholder

prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template("You are Alice from ALices wonderland"),
    HumanMessagePromptTemplate.from_template("{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad")
])

from langchain.agents import create_openai_tools_agent

agent = create_openai_tools_agent(llm, tools, prompt)

from langchain.agents import AgentExecutor
agent_executer = AgentExecutor(agent=agent, tools=tools, verbose=True)
agent_executer

agent_executer.invoke({"input":"What is your favorite actiivty?"})

from langchain.agents import create_openai_tools_agent, AgentExecutor
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate, MessagesPlaceholder

# Your existing code for setting up tools, LLM, etc.
# ...

app = FastAPI(
    title="Alice's Wonderland Characters",
    version="1.0",
    description="An API to interact with Alice's Wonderland characters"
)

characters = ["Alice", "White Rabbit", "Mad Hatter", "Cheshire Cat", "Queen of Hearts"]
description = ["Alice responds to the user with curiosity and politeness, often asking questions and seeking explanations while maintaining a sense of wonder and imagination.", 
               "he White Rabbit, always in a hurry and concerned about being late, provides brief and to-the-point answers, frequently mentioning time and schedules, and may seem distracted or preoccupied.",
               "The Mad Hatter engages in wordplay and riddles, giving eccentric and unconventional responses that may seem nonsensical or illogical, while enjoying tea parties and discussing peculiar topics",
               "The Cheshire Cat speaks in riddles and paradoxes, offering mysterious and thought-provoking answers, and may appear and disappear unexpectedly.",
               'The Queen of Hearts, with an authoritative and demanding demeanor, responds with a sense of superiority and impatience, issuing commands and threats, and is prone to anger and shouting "Off with their head!"']
def get_agent_executor(character, index):
    prompt = ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate.from_template(f"You are {character} from Alice's Wonderland. {description[index]}"),
        HumanMessagePromptTemplate.from_template("{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad")
    ])

    agent = create_openai_tools_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    return agent_executor

agent_executors = {character: get_agent_executor(character, index) for index, character in enumerate(characters)}

class PromptRequest(BaseModel):
    prompt: str

@app.post("/alice")
async def alice_route(request: PromptRequest):
    return agent_executors["Alice"].invoke({"input": request.prompt})

@app.post("/white-rabbit")
async def white_rabbit_route(request: PromptRequest):
    return agent_executors["White Rabbit"].invoke({"input": request.prompt})

@app.post("/mad-hatter")
async def mad_hatter_route(request: PromptRequest):
    return agent_executors["Mad Hatter"].invoke({"input": request.prompt})

@app.post("/cheshire-cat")
async def cheshire_cat_route(request: PromptRequest):
    return agent_executors["Cheshire Cat"].invoke({"input": request.prompt})

@app.post("/queen-of-hearts")
async def queen_of_hearts_route(request: PromptRequest):
    return agent_executors["Queen of Hearts"].invoke({"input": request.prompt})
