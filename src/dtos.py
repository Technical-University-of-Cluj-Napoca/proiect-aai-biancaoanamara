from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from enum import Enum

class SeverityLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

class FeedbackStatus(str, Enum):
    TRUE_POSITIVE = "TRUE_POSITIVE"
    FALSE_POSITIVE = "FALSE_POSITIVE"

class FunctionDTO(BaseModel):
    name: str
    start_line: int
    end_line: int
    code_snippet: str
    cyclomatic_complexity: Optional[int] = None

class CodeFileDTO(BaseModel):
    file_path: str
    content: str
    functions: List[FunctionDTO] = Field(default_factory=list)
    language: str = "python"

class RepositoryDTO(BaseModel):
    repo_url: str
    files: List[CodeFileDTO] = Field(default_factory=list)
    dependencies: List[str] = Field(default_factory=list)

class VulnerabilityDTO(BaseModel):
    vulnerability_id: str = Field(description="Internal or CVE/CWE ID")
    description: str
    severity: SeverityLevel
    file_path: str
    line_number: Optional[int] = None
    code_snippet: Optional[str] = None
    remediation: str
    false_positive: bool = False

class CodeSmellDTO(BaseModel):
    smell_type: str
    description: str
    file_path: str
    line_number: Optional[int] = None
    severity: SeverityLevel = SeverityLevel.LOW

class DependencyRiskDTO(BaseModel):
    dependency_name: str
    current_version: str
    vulnerability_details: str
    severity: SeverityLevel

class RetrievalResultDTO(BaseModel):
    source_document: str
    content: str
    relevance_score: float

class FileReviewDTO(BaseModel):
    file_path: str
    vulnerabilities: List[VulnerabilityDTO] = Field(default_factory=list)
    code_smells: List[CodeSmellDTO] = Field(default_factory=list)

class FeedbackDTO(BaseModel):
    vulnerability_id: str
    file_path: str
    status: FeedbackStatus
    user_comments: Optional[str] = None

class ReviewReportDTO(BaseModel):
    repository_url: str
    file_reviews: List[FileReviewDTO] = Field(default_factory=list)
    dependency_risks: List[DependencyRiskDTO] = Field(default_factory=list)
    summary: str
