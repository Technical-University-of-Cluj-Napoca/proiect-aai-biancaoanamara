import sys
import os
from dotenv import load_dotenv

load_dotenv()
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.tools.vector_tools import search_main_vectorstore

def evaluate():
    print("Running retrieval evaluation...")
    queries = [
        "What is SQL Injection and how to prevent it?",
        "Explain Cross-Site Scripting (XSS).",
        "How to securely store passwords in Python?"
    ]
    
    for query in queries:
        print(f"\nQuery: {query}")
        results = search_main_vectorstore(query, k=2)
        if not results:
            print("  No results found. (Did you run build_index.py?)")
        for i, res in enumerate(results):
            print(f"  Result {i+1} [{res.metadata.get('source', 'unknown')}]: {res.page_content[:100]}...")

if __name__ == "__main__":
    evaluate()
