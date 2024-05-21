from langchain_community.document_loaders import WebBaseLoader, PyPDFLoader

def load_web_data(url):
    return WebBaseLoader(url).load()

def load_pdf_data(file_path):
    return PyPDFLoader(file_path).load()