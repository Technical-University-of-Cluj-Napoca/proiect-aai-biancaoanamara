import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from src.dtos import FileReviewDTO, VulnerabilityDTO, SeverityLevel
from src.tools.vector_tools import search_main_vectorstore

def scan_file_for_vulnerabilities(file_path: str, file_content: str) -> FileReviewDTO:
    """Uses LLM and RAG to find security vulnerabilities in a file."""
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    
    # Simple RAG: query for general python vulnerabilities or specific things in code
    # For a real system, we might query based on extracted keywords
    rag_docs = search_main_vectorstore("python security vulnerabilities OWASP CWE", k=3)
    context = "\n".join([doc.page_content for doc in rag_docs])
    
    prompt = PromptTemplate(
        template="""You are an expert secure code reviewer.
        Analyze the following Python file for security vulnerabilities.
        Use the provided context to identify CVEs or OWASP Top 10 issues.
        
        Context:
        {context}
        
        File: {file_path}
        Content:
        {file_content}
        
        Return the vulnerabilities as a JSON array where each object has:
        - vulnerability_id (string)
        - description (string)
        - severity (LOW, MEDIUM, HIGH, CRITICAL)
        - line_number (integer, optional)
        - code_snippet (string)
        - remediation (string)
        """,
        input_variables=["context", "file_path", "file_content"]
    )
    
    chain = prompt | llm.with_structured_output(FileReviewDTO)
    
    try:
        result = chain.invoke({
            "context": context,
            "file_path": file_path,
            "file_content": file_content
        })
        # The result might be a dict depending on structured output, but let's assume it parses into FileReviewDTO.
        # Actually with_structured_output parses into the Pydantic model directly.
        
        # We ensure file_path is correct
        result.file_path = file_path
        return result
    except Exception as e:
        print(f"Error scanning {file_path}: {e}")
        return FileReviewDTO(file_path=file_path, vulnerabilities=[])
