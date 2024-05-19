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
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory



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


# Arxiv Tool search: for academic papers

arxiv_wrapper = ArxivAPIWrapper(top_k_results=TOP_K_RESULTS,document_content_chars_max=DOCUMENT_CONTENT_CHARS_MAX)
arxiv = ArxivQueryRun(arxiv_wrapper = arxiv_wrapper)

#creating the prompt for the agent
#if the agent doenst find the information on wiki, it goes to retriever_tool then arxiv - different sources making this a multimodal agent

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)



prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You're {character} from the book Alice's Wonderland. Respond in 20 words or fewer.",
        ),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}"),
    ]
)
runnable = prompt | llm

store = {}


def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

#
with_message_history = RunnableWithMessageHistory(
    runnable,
    get_session_history,
    input_messages_key="input",
    history_messages_key="history",
)

with_message_history.invoke(
    {"character": "math", "input": "What does cosine mean?"},
    config={"configurable": {"session_id": "abc123"}},
)

print(store)