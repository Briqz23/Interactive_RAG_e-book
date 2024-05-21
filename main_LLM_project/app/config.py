import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Configurações
TOP_K_RESULTS = 1
DOCUMENT_CONTENT_CHARS_MAX = 400
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

# Chaves de API
LANGCHAIN_API_KEY = os.getenv('LANGCHAIN_API_KEY', 'nao encontrada')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', 'nao encontrada')

# Configurações de ambiente
os.environ['LANGCHAIN_TRACING_V2'] = 'true'
os.environ['LANGCHAIN_API_KEY'] = LANGCHAIN_API_KEY
os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY