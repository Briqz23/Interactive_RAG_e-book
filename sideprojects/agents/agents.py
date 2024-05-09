import arxiv
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper

api_wrapper = WikipediaAPIWrapper(top_k_results=1,document_content_chars_max=200)   
wiki = WikipediaQueryRun(api_wrapper = api_wrapper)
wiki.name

from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter


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

##Arxiv Tool

from langchain_community.utilities import ArxivAPIWrapper
from langchain_community.tools import ArxivQueryRun

arxiv_wrapper = ArxivAPIWrapper(top_k_results=1,document_content_chars_max=200)
arxiv = ArxivQueryRun(arxiv_wrapper = arxiv_wrapper)

tools = [wiki, retriever_tool, arxiv] #if it doesnt get the info on tool, tru on retirever, then arxiv
tools

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY', 'nao encontraaada')

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

#criando o prompt de uma forma diferente - pegando da comunidade

from langchain import hub
#https://smith.langchain.com/hub/rlm/rag-prompt
prompt = hub.pull("hwchase17/openai-functions-agent")
prompt.messages

from langchain.agents import create_openai_tools_agent

agent = create_openai_tools_agent(llm, tools, prompt)

from langchain.agents import AgentExecutor
agent_executer = AgentExecutor(agent=agent, tools=tools, verbose=True)
agent_executer

agent_executer.invoke({"input":"Alice, what is your story?."})