from radon.complexity import cc_visit
from src.dtos import CodeFileDTO, CodeSmellDTO, SeverityLevel


def analyze_quality(code_file: CodeFileDTO) -> list[CodeSmellDTO]:
    """Analyze a Python file to identify code quality issues."""
    smells = []

    # 1. Cyclomatic complexity analysis using radon
    try:
        # cc_visit returns complexity info for each function/class
        blocks = cc_visit(code_file.content)

        for block in blocks:
            # Threshold 10 is standard for high complexity
            if block.complexity > 10:
                smells.append(
                    CodeSmellDTO(
                        smell_type="HIGH_COMPLEXITY",
                        description=(
                            f"Function '{block.name}' has complexity "
                            f"{block.complexity}. Refactoring recommended."
                        ),
                        file_path=code_file.file_path,
                        line_number=block.lineno,
                        severity=SeverityLevel.MEDIUM,
                    )
                )

    except SyntaxError:
        # Skip files that cannot be parsed
        pass

    # 2. Quality score calculation (per section 6.5)
    # Formula:
    # 100 - (n_CRITICAL*25) - (n_HIGH*10) - (n_MED*5) - (n_LOW*1)
    # Can be implemented and attached to final review output

    return smells