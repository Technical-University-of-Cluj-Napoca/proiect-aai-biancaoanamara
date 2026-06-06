from typing import TypedDict, List
from langgraph.graph import StateGraph, START, END

from src.dtos import RepositoryDTO, FileReviewDTO
from src.tools.repo_tools import clone_repo
from src.agents.parser_agent import parse_repository
from src.agents.security_agent import scan_file_for_vulnerabilities
from src.agents.quality_agent import analyze_quality
from src.agents.feedback_agent import apply_feedback_memory
from src.agents.report_agent import generate_report

class WorkflowState(TypedDict):
    repo_url: str
    repo_path: str
    repository: RepositoryDTO
    reviews: List[FileReviewDTO]
    final_report: str

def clone_and_parse_node(state: WorkflowState) -> WorkflowState:
    print(f"--- Cloning and Parsing Repo: {state['repo_url']} ---")
    repo_path = clone_repo(state['repo_url'])
    repository = parse_repository(repo_path, state['repo_url'])
    
    return {
        **state,
        "repo_path": repo_path,
        "repository": repository
    }

def scan_node(state: WorkflowState) -> WorkflowState:
    print("--- Scanning for Security and Quality ---")
    repository = state["repository"]
    reviews = []
    
    for file_dto in repository.files:
        print(f"Scanning file: {file_dto.file_path}")
        # Security scan
        review = scan_file_for_vulnerabilities(file_dto.file_path, file_dto.content)
        
        # Quality scan
        smells = analyze_quality(file_dto)
        review.code_smells = smells
        
        # Feedback agent (episodic memory check)
        review = apply_feedback_memory(review)
        
        reviews.append(review)
        
    return {
        **state,
        "reviews": reviews
    }

def report_node(state: WorkflowState) -> WorkflowState:
    print("--- Generating Final Report ---")
    report = generate_report(state["repository"], state["reviews"])
    return {
        **state,
        "final_report": report
    }

def create_workflow():
    workflow = StateGraph(WorkflowState)
    
    workflow.add_node("clone_and_parse", clone_and_parse_node)
    workflow.add_node("scan", scan_node)
    workflow.add_node("report", report_node)
    
    workflow.add_edge(START, "clone_and_parse")
    workflow.add_edge("clone_and_parse", "scan")
    workflow.add_edge("scan", "report")
    workflow.add_edge("report", END)
    
    return workflow.compile()
