import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.tools.vector_tools import search_main_vectorstore

if __name__ == "__main__":
    if len(sys.argv) > 1:
        query = sys.argv[1]
    else:
        query = "SQL Injection prevention"
        
    print(f"Testing retrieval for query: '{query}'")
    results = search_main_vectorstore(query, k=3)
    if not results:
        print("No results. Make sure ChromaDB is populated via build_index.py.")
    else:
        for i, res in enumerate(results):
            print(f"\n--- Result {i+1} ---")
            print(f"Source: {res.metadata.get('source', 'Unknown')}")
            print(f"Content: {res.page_content}")
