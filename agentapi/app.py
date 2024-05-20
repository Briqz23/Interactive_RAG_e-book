import arxiv
from langchain_community.tools import WikipediaQueryRun, ArxivQueryRun
from langchain_community.utilities import WikipediaAPIWrapper, ArxivAPIWrapper
from langchain_community.document_loaders import WebBaseLoader, PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.tools.retriever import create_retriever_tool
from fastapi import FastAPI
from pydantic import BaseModel
from langchain.agents import create_openai_tools_agent, AgentExecutor
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate, MessagesPlaceholder
import os
from dotenv import load_dotenv

from langchain.chains import create_history_aware_retriever
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder


# Constants
TOP_K_RESULTS = 1
DOCUMENT_CONTENT_CHARS_MAX = 400
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

# Load environment variables

load_dotenv()
os.environ['LANGCHAIN_TRACING_V2'] = 'true'
os.environ['LANGCHAIN_API_KEY'] = os.getenv('LANGCHAIN_API_KEY', 'nao encontrada')
os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY', 'nao encontraaada')


#  Using API for wikipedia content - this will later be implemented in the "tools" for the agent

api_wrapper = WikipediaAPIWrapper(top_k_results=TOP_K_RESULTS,document_content_chars_max=DOCUMENT_CONTENT_CHARS_MAX)   
wiki = WikipediaQueryRun(api_wrapper = api_wrapper)


# Loading the content from the web and splitting the text into chunks to be used in the FAISS
# PDF loader and splitting the text into chunks to be used in the FAISS
def load_and_split(loader, splitter, embeddings):
    docs = loader.load()
    documents = splitter.split_documents(docs)
    db = FAISS.from_documents(documents, embeddings)
    return db

web_db = load_and_split(WebBaseLoader("https://www.studypool.com/studyGuides/Alice_in_Wonderland/Characters"), 
                          RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP), 
                          OpenAIEmbeddings())

pdf_db = load_and_split(PyPDFLoader('alice_in_wonderland.pdf'), 
                        RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP), 
                        OpenAIEmbeddings())


def combine_databases(db1, db2):
    db1.merge_from(db2)
    return db1

vectordb = combine_databases(web_db, pdf_db)



# Create a retriever interface to interact with the FAISS vector database and retrieve relevant documents based on queries.

retriever = vectordb.as_retriever() 
retriever

# creating the retriever tool as in https://api.python.langchain.com/en/latest/tools/langchain.tools.retriever.create_retriever_tool.html 
# this tool will be used to query for information in the FAISS database

retriever_tool = create_retriever_tool(retriever, "langsmith_search", "search about information regarding Alice in Wonderland. Try to trace a personality she might have met in the story.")
retriever_tool.name


# Arxiv Tool search: for academic papers

arxiv_wrapper = ArxivAPIWrapper(top_k_results=TOP_K_RESULTS,document_content_chars_max=DOCUMENT_CONTENT_CHARS_MAX)
arxiv = ArxivQueryRun(arxiv_wrapper = arxiv_wrapper)

#creating the prompt for the agent
#if the agent doenst find the information on wiki, it goes to retriever_tool then arxiv - different sources making this a multimodal agent

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
tools = [wiki, retriever_tool, arxiv] 
#agent prompt
contextualize_q_prompt = ChatPromptTemplate.from_messages([
    MessagesPlaceholder("chat_history"),
    SystemMessagePromptTemplate.from_template("You are an AI agent in the context of Alices wonderland characters."),
    HumanMessagePromptTemplate.from_template("{input}"), #input = question
    MessagesPlaceholder(variable_name="agent_scratchpad")
])
history_aware_retriever = create_history_aware_retriever(
    llm, retriever, contextualize_q_prompt
)

agent = create_openai_tools_agent(llm, tools, contextualize_q_prompt)
agent_executer = AgentExecutor(agent=agent, tools=tools, verbose=True)


#creating the API
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
chat_history = []
def get_agent_executor(character, index) -> AgentExecutor:
    prompt = ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate.from_template(f"You are {character} from Alice's Wonderland. {description[index]}. Also use the {chat_history} to provide context for next answer."),
        HumanMessagePromptTemplate.from_template("{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad")
    ])

    agent = create_openai_tools_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    return agent_executor

agent_executors = {character: get_agent_executor(character, index) for index, character in enumerate(characters)}

class PromptRequest(BaseModel):
    prompt: str

def create_endpoint(character: str):
    async def endpoint(request: PromptRequest):
        return agent_executors[character].invoke({"input": request.prompt})
    return endpoint

app.post("/alice")(create_endpoint("Alice"))
app.post("/white-rabbit")(create_endpoint("White Rabbit"))
app.post("/mad-hatter")(create_endpoint("Mad Hatter"))
app.post("/cheshire-cat")(create_endpoint("Cheshire Cat"))
app.post("/queen-of-hearts")(create_endpoint("Queen of Hearts"))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)