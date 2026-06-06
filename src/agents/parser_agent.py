import ast
from src.tools.repo_tools import list_python_files, read_file_content
from src.dtos import RepositoryDTO, CodeFileDTO, FunctionDTO

def parse_repository(repo_path: str, repo_url: str) -> RepositoryDTO:
    """Parses a repository and extracts functions using AST."""
    py_files = list_python_files(repo_path)
    code_files = []
    
    for file_path in py_files:
        content = read_file_content(file_path)
        if not content:
            continue
            
        try:
            tree = ast.parse(content)
        except SyntaxError:
            continue
            
        functions = []
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                start = node.lineno
                end = node.end_lineno
                snippet_lines = content.split("\n")[start-1:end]
                code_snippet = "\n".join(snippet_lines)
                
                functions.append(FunctionDTO(
                    name=node.name,
                    start_line=start,
                    end_line=end,
                    code_snippet=code_snippet
                ))
                
        code_files.append(CodeFileDTO(
            file_path=file_path,
            content=content,
            functions=functions,
            language="python"
        ))
        
    return RepositoryDTO(repo_url=repo_url, files=code_files, dependencies=[])
