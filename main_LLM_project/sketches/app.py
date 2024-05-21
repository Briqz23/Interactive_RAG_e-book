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

# Using API for Wikipedia content
api_wrapper = WikipediaAPIWrapper(top_k_results=TOP_K_RESULTS, document_content_chars_max=DOCUMENT_CONTENT_CHARS_MAX)
wiki = WikipediaQueryRun(api_wrapper=api_wrapper)

# Loading the content from the web and splitting the text into chunks to be used in the FAISS
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

# Creating the retriever tool
retriever_tool = create_retriever_tool(retriever, "langsmith_search", "search about information regarding Alice in Wonderland. Try to trace a personality she might have met in the story.")

# Arxiv Tool search: for academic papers
arxiv_wrapper = ArxivAPIWrapper(top_k_results=TOP_K_RESULTS, document_content_chars_max=DOCUMENT_CONTENT_CHARS_MAX)
arxiv = ArxivQueryRun(arxiv_wrapper=arxiv_wrapper)

# Creating the prompt for the agents
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
tools = [wiki, retriever_tool, arxiv]

characters = ["Alice", "White Rabbit", "Mad Hatter", "Cheshire Cat", "Queen of Hearts"]
descriptions = [
    "Alice responds with curiosity and politeness, asking questions and seeking explanations. She does not answer unrelated subjects.",
    "The White Rabbit, always in a hurry and concerned about time, gives brief and to-the-point answers, frequently mentioning schedules. He does not answer unrelated subjects.",
    "The Mad Hatter engages in wordplay and riddles, giving eccentric and unconventional responses. He does not answer unrelated subjects.",
    "The Cheshire Cat speaks in riddles and paradoxes, offering mysterious and thought-provoking answers. He does not answer unrelated subjects.",
    "The Queen of Hearts, with an authoritative and impatient demeanor, responds with superiority and impatience, issuing commands and threats. She does not answer unrelated subjects."
]

def get_agent_executor(character, index) -> AgentExecutor:
    prompt = ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate.from_template(f"You are {character} from Alice's Wonderland. {descriptions[index]}"),
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

app = FastAPI(
    title="Alice's Wonderland Characters",
    version="1.0",
    description="An API to interact with Alice's Wonderland characters"
)

app.post("/alice")(create_endpoint("Alice"))
app.post("/white-rabbit")(create_endpoint("White Rabbit"))
app.post("/mad-hatter")(create_endpoint("Mad Hatter"))
app.post("/cheshire-cat")(create_endpoint("Cheshire Cat"))
app.post("/queen-of-hearts")(create_endpoint("Queen of Hearts"))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)