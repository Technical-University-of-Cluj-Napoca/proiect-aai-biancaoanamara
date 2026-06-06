from src.dtos import FileReviewDTO
from src.tools.vector_tools import search_memory_vectorstore
import json

def apply_feedback_memory(review: FileReviewDTO) -> FileReviewDTO:
    """
    Checks the episodic memory vectorstore to see if any of the found vulnerabilities
    were previously marked as FALSE_POSITIVE.
    """
    filtered_vulns = []
    
    for vuln in review.vulnerabilities:
        # Create a signature for the vulnerability to search in memory
        query = f"Vulnerability {vuln.vulnerability_id} in {review.file_path}: {vuln.description}"
        results = search_memory_vectorstore(query, k=1)
        
        is_false_positive = False
        if results:
            # Try to parse the stored metadata or content
            try:
                memory_data = json.loads(results[0].page_content)
                if memory_data.get("status") == "FALSE_POSITIVE" and memory_data.get("vulnerability_id") == vuln.vulnerability_id:
                    print(f"Memory matched: {vuln.vulnerability_id} is a known false positive.")
                    is_false_positive = True
            except:
                pass
                
        if not is_false_positive:
            filtered_vulns.append(vuln)
        else:
            vuln.false_positive = True
            filtered_vulns.append(vuln)
            
    review.vulnerabilities = filtered_vulns
    return review

def save_feedback(vulnerability_id: str, file_path: str, status: str, comments: str = ""):
    """Saves user feedback to the memory vectorstore."""
    from langchain.docstore.document import Document
    from src.tools.vector_tools import get_memory_vectorstore
    
    data = {
        "vulnerability_id": vulnerability_id,
        "file_path": file_path,
        "status": status,
        "comments": comments
    }
    
    doc = Document(
        page_content=json.dumps(data),
        metadata={"source": "user_feedback"}
    )
    
    vectorstore = get_memory_vectorstore()
    vectorstore.add_documents([doc])
