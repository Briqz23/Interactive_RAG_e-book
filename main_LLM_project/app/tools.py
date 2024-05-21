from langchain_community.tools import WikipediaQueryRun, ArxivQueryRun
from langchain_community.utilities import WikipediaAPIWrapper, ArxivAPIWrapper
from langchain.tools.retriever import create_retriever_tool

def create_wikipedia_tool(top_k_results, document_content_chars_max):
    api_wrapper = WikipediaAPIWrapper(top_k_results=top_k_results, document_content_chars_max=document_content_chars_max)
    return WikipediaQueryRun(api_wrapper=api_wrapper)

def create_arxiv_tool(top_k_results, document_content_chars_max):
    arxiv_wrapper = ArxivAPIWrapper(top_k_results=top_k_results, document_content_chars_max=document_content_chars_max)
    return ArxivQueryRun(arxiv_wrapper=arxiv_wrapper)

def create_retriever_tool_from_db(vectordb, tool_name, description):
    retriever = vectordb.as_retriever()
    return create_retriever_tool(retriever, tool_name, description)