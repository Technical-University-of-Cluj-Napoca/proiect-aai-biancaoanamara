from enum import Enum
from pydantic import BaseModel
from typing import List, Optional

# Define the severity levels for vulnerabilities
class VulnerabilitySeverity(str, Enum):
    CRITICAL = "CRITIC"
    HIGH = "RIDICAT"
    MEDIUM = "MEDIU"
    LOW = "SCAZUT"
    INFO = "INFO"

# Define the types of issues the agents can find
class IssueType(str, Enum):
    SECURITY_VULN = "SECURITY_VULN"
    CODE_SMELL = "CODE_SMELL"
    STYLE_VIOLATION = "STYLE_VIOLATION"
    DEPENDENCY_RISK = "DEPENDENCY_RISK"
    LOGIC_ERROR = "LOGIC_ERROR"
    HARDCODED_SECRET = "HARDCODED_SECRET"

# Define the programming languages supported by the system
class Language(str, Enum):
    PYTHON = "PYTHON"
    JAVASCRIPT = "JAVASCRIPT"
    TYPESCRIPT = "TYPESCRIPT"
    JAVA = "JAVA"
    GO = "GO"
    OTHER = "OTHER"

# DTO for representing a specific function parsed from the code
class FunctionDTO(BaseModel):
    name: str
    start_line: int
    end_line: int
    params: List[str]
    cyclomatic_complexity: Optional[float] = None

# DTO for representing a complete code file
class CodeFileDTO(BaseModel):
    file_path: str
    language: Language
    content: str
    lines_of_code: int
    functions: List[FunctionDTO]
    imports: List[str]
    dependencies: List[str]


# DTO for representing the entire parsed repository
class RepositoryDTO(BaseModel):
    url: str
    name: str
    local_path: str
    files: List[CodeFileDTO]
    total_loc: int
    languages: List[Language]