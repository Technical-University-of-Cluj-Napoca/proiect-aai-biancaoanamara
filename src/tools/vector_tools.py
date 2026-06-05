import os
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

# Define paths for the vector stores
MAIN_CHROMA_DIR = "vectorstore/main"
MEMORY_CHROMA_DIR = "memory/chroma"

def get_embeddings():
    """Returns the OpenAI embeddings model."""
    # We use text-embedding-3-small as default
    return OpenAIEmbeddings(model="text-embedding-3-small")

def get_main_vectorstore() -> Chroma:
    """Returns the main ChromaDB vector store used for CVEs/OWASP RAG."""
    os.makedirs(MAIN_CHROMA_DIR, exist_ok=True)
    return Chroma(
        persist_directory=MAIN_CHROMA_DIR,
        embedding_function=get_embeddings()
    )

def get_memory_vectorstore() -> Chroma:
    """Returns the episodic memory ChromaDB vector store used for user feedback."""
    os.makedirs(MEMORY_CHROMA_DIR, exist_ok=True)
    return Chroma(
        persist_directory=MEMORY_CHROMA_DIR,
        embedding_function=get_embeddings()
    )

def add_documents_to_main(documents):
    """Adds LangChain Documents to the main vectorstore and persists."""
    vectorstore = get_main_vectorstore()
    vectorstore.add_documents(documents)

def search_main_vectorstore(query: str, k: int = 5):
    """Searches the main vectorstore for the query."""
    vectorstore = get_main_vectorstore()
    return vectorstore.similarity_search(query, k=k)

def search_memory_vectorstore(query: str, k: int = 3):
    """Searches the episodic memory vectorstore for the query."""
    vectorstore = get_memory_vectorstore()
    return vectorstore.similarity_search(query, k=k)
