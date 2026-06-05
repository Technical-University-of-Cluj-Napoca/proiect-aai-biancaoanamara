from radon.complexity import cc_visit
from src.dtos import CodeFileDTO, CodeSmellDTO, SeverityLevel

def analyze_quality(code_file: CodeFileDTO) -> list[CodeSmellDTO]:
    """Analyzes a python file for code smells and cyclomatic complexity."""
    smells = []
    
    try:
        blocks = cc_visit(code_file.content)
        for block in blocks:
            # Cyclomatic complexity check
            if block.complexity > 10:
                smells.append(CodeSmellDTO(
                    smell_type="High Cyclomatic Complexity",
                    description=f"Function '{block.name}' has a complexity of {block.complexity}. Consider refactoring.",
                    file_path=code_file.file_path,
                    line_number=block.lineno,
                    severity=SeverityLevel.MEDIUM
                ))
    except SyntaxError:
        pass
        
    # We could also use an LLM for deeper code smells like "Magic Numbers" or "Long Methods"
    
    return smells
