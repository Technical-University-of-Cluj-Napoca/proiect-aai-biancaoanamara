import os
import sys
from dotenv import load_dotenv
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from src.tools.vector_tools import add_documents_to_main

load_dotenv()

CORPUS_DIR = "corpus"

def build_index():
    if not os.path.exists(CORPUS_DIR):
        print(f"Corpus directory '{CORPUS_DIR}' does not exist. Create it and add .txt or .md files.")
        return

    print(f"Loading documents from {CORPUS_DIR}...")
    # Load markdown and text files
    loader = DirectoryLoader(CORPUS_DIR, glob="**/*.*", loader_cls=TextLoader, use_multithreading=True, silent_errors=True)
    try:
        documents = loader.load()
    except Exception as e:
        print(f"Failed to load documents: {e}")
        return

    if not documents:
        print("No documents found in the corpus directory.")
        return

    print(f"Loaded {len(documents)} documents. Splitting text...")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    docs = text_splitter.split_documents(documents)

    print(f"Adding {len(docs)} chunks to ChromaDB...")
    add_documents_to_main(docs)
    print("Done building index!")

if __name__ == "__main__":
    # Ensure src is in the python path
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    build_index()
