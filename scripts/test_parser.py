import ast
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.dtos import CodeFileDTO, FunctionDTO

def parse_python_file(file_path: str) -> CodeFileDTO:
    """A basic parser that will later be moved to the parser agent."""
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    tree = ast.parse(content)
    functions = []
    
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            start = node.lineno
            end = node.end_lineno
            code_snippet = "\n".join(content.split("\n")[start-1:end])
            
            functions.append(FunctionDTO(
                name=node.name,
                start_line=start,
                end_line=end,
                code_snippet=code_snippet,
                cyclomatic_complexity=None # We'll compute this in the quality agent
            ))
            
    return CodeFileDTO(
        file_path=file_path,
        content=content,
        functions=functions,
        language="python"
    )

if __name__ == "__main__":
    print("Testing parser on itself...")
    file_dto = parse_python_file(__file__)
    print(f"Parsed {file_dto.file_path}")
    for func in file_dto.functions:
        print(f" - Function: {func.name} (Lines: {func.start_line}-{func.end_line})")
