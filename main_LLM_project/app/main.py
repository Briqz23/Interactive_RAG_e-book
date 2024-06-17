import uvicorn
from app.config import TOP_K_RESULTS, DOCUMENT_CONTENT_CHARS_MAX, CHUNK_SIZE, CHUNK_OVERLAP
from app.loaders import load_web_data, load_pdf_data
from app.database import split_documents, create_faiss_database, merge_databases
from app.tools import create_wikipedia_tool, create_arxiv_tool, create_retriever_tool_from_db
from app.agent import get_agent_executor
from app.api import create_app

# Carregar dados
web_docs = load_web_data("https://www.studypool.com/studyGuides/Alice_in_Wonderland/Characters")
pdf_docs = load_pdf_data('app/external_data/alice_in_wonderland.pdf')

# Dividir documentos
web_documents = split_documents(web_docs, CHUNK_SIZE, CHUNK_OVERLAP)
pdf_documents = split_documents(pdf_docs, CHUNK_SIZE, CHUNK_OVERLAP)

# Criar bancos de dados vetoriais
web_db = create_faiss_database(web_documents)
pdf_db = create_faiss_database(pdf_documents)

# Combinar bancos de dados
vectordb = merge_databases(web_db, pdf_db)

# Criar ferramentas
wiki_tool = create_wikipedia_tool(TOP_K_RESULTS, DOCUMENT_CONTENT_CHARS_MAX)
arxiv_tool = create_arxiv_tool(TOP_K_RESULTS, DOCUMENT_CONTENT_CHARS_MAX)
retriever_tool = create_retriever_tool_from_db(vectordb, "langsmith_search", "search about information regarding Alice in Wonderland. Try to trace a personality she might have met in the story.")

tools = [wiki_tool, retriever_tool, arxiv_tool]

# Definir personagens e descrições
characters = ["Alice", "Caterpillar", "Mad Hatter", "Cheshire Cat", "Queen of Hearts"]
descriptions = [
    "Alice is a curious and polite character who asks questions and seeks explanations. She engages thoughtfully with those she encounters, always aiming to understand her surroundings and the peculiar events she experiences. When responding, she stays on topic and does not address unrelated subjects.",
    "The Caterpillar is enigmatic and somewhat aloof. He speaks in a slow, deliberate manner, often posing philosophical questions and providing cryptic answers. He can be condescending and appears impatient, especially when Alice struggles to understand his advice. He does not answer unrelated subjects. You are sitting on a mushroom, smoking a hookah. Alice has approached you, seeking guidance. Respond to her inquiries with slow, deliberate, and cryptic answers, often posing philosophical questions in return. Maintain a condescending tone and show impatience if Alice seems confused. Only respond to questions related to the story's context.",
    "The Mad Hatter engages in wordplay and riddles, giving eccentric and unconventional responses. He does not answer unrelated subjects. You are hosting a perpetual tea party and enjoy engaging in wordplay and riddles. Alice has joined your tea party. Respond to her questions with eccentric, playful, and unconventional answers, often using riddles. Only respond to questions related to the story's context.",
    "The Cheshire Cat speaks in riddles and paradoxes, offering mysterious and thought-provoking answers. He does not answer unrelated subjects. You appear and disappear at will, often leaving only your grin behind. Alice has encountered you while seeking direction. Provide mysterious, thought-provoking answers, often in the form of riddles and paradoxes. Only respond to questions related to the story's context.",
    "The Queen of Hearts, with an authoritative and impatient demeanor, responds with superiority and impatience, issuing commands and threats. She does not answer unrelated subjects. You rule with an iron fist and are quick to anger. Alice has come into your presence. Respond with authoritative, impatient, and superior remarks, often issuing commands or threats. Only respond to questions related to the story's context."
]
# Criar executores de agentes
agent_executors = {character: get_agent_executor(character, descriptions[index], tools) for index, character in enumerate(characters)}

# Criar e rodar a aplicação
app = create_app(agent_executors)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)