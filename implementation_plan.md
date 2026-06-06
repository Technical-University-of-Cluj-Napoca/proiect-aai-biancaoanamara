# Agentic AI Code Review and Security Vulnerability Detection System

This implementation plan outlines the steps to build a multi-agent system capable of taking a GitHub repository URL, analyzing its source code for security vulnerabilities and code quality issues, and producing a structured report. The system uses RAG to ground security findings in real CVE/OWASP data and incorporates episodic memory to learn from human feedback.

## User Review Required

> [!IMPORTANT]  
> Please review this plan to ensure it covers all the requirements from the `Proiect_AAI - cybersecurity 1.pdf` document. Given the scale of this project, I will execute the implementation in phases.

## Open Questions

> [!WARNING]  
> - **API Keys:** The system requires `OPENAI_API_KEY` (and optionally `GITHUB_TOKEN`, `NVD_API_KEY`). Please confirm you will configure these in the `.env` file once the template is created.
> - **Vector Database:** We will use `ChromaDB` for the vectorstore. Since embedding models are needed, `text-embedding-3-small` (or `code-embedding-ada-002`) will be used. Do you have a preference?
> - **LLM:** We will default to `gpt-4o-mini` as suggested.

## Proposed Changes

We will create the complete folder structure and necessary scripts inside the `d:\BIANCA` directory.

### 1. Configuration & Infrastructure
We will setup the root files for environments, docker, and python dependencies.
- **[NEW]** `requirements.txt`: FastAPI, Streamlit, LangChain, LangGraph, ChromaDB, Pydantic, GitPython, Radon, Vulture, Jupyter, etc.
- **[NEW]** `.gitignore`: Exclude `.env`, `vectorstore/`, `memory/`, `data/repos/`, `__pycache__/`, etc.
- **[NEW]** `.env.example`: Template for API keys.
- **[NEW]** `Dockerfile` & `docker-compose.yml`: For containerizing the Streamlit app and mounting persistent volumes for the vectorstores.

---

### 2. Data Transfer Objects (DTOs)
Central definitions using Pydantic to ensure reliable communication between agents.
- **[NEW]** `src/dtos.py`: `FunctionDTO`, `CodeFileDTO`, `RepositoryDTO`, `VulnerabilityDTO`, `CodeSmellDTO`, `DependencyRiskDTO`, `RetrievalResultDTO`, `FileReviewDTO`, `FeedbackDTO`, `ReviewReportDTO`, and relevant Enums.

---

### 3. Tooling & Setup Scripts
Tools for fetching code and managing the vector databases.
- **[NEW]** `src/tools/repo_tools.py`: Functions to clone Git repos (`clone_repo`), list files, and read content.
- **[NEW]** `src/tools/vector_tools.py`: Functions to initialize and query the main ChromaDB and the episodic memory ChromaDB.
- **[NEW]** `scripts/build_index.py`: Script to parse documents from `corpus/` and index them into `vectorstore/`.
- **[NEW]** `scripts/evaluate_rag.py`: Script using RAGAS to evaluate the retriever on 10 predefined questions.
- **[NEW]** `scripts/test_parser.py` & `scripts/test_retrieval.py`: Test scripts for individual agents.

---

### 4. Agents Implementation
Implementation of the specialized LangChain agents.
- **[NEW]** `src/agents/parser_agent.py`: Parses the repository using Python `ast` and `regex` to extract structure into `RepositoryDTO`.
- **[NEW]** `src/agents/security_agent.py`: Performs RAG-based security scans on files, cross-referencing with the vectorstore.
- **[NEW]** `src/agents/quality_agent.py`: Uses `radon` for cyclomatic complexity and detects code smells like "Long Method", "Magic Numbers", etc.
- **[NEW]** `src/agents/feedback_agent.py`: Manages the episodic memory, persisting `FeedbackDTO` and injecting relevant past feedback into the context.
- **[NEW]** `src/agents/report_agent.py`: Aggregates all DTOs into a comprehensive Markdown report.

---

### 5. LangGraph Orchestration
- **[NEW]** `src/graph/workflow.py`: Defines the `StateGraph` with states (`parse_repo`, `augment_with_memory`, `security_scan`, `quality_check_node`, `coverage_check`, `generate_report`) and conditional routing.

---

### 6. User Interface & Demonstration
- **[NEW]** `src/app.py`: Streamlit application allowing users to input a repository URL, view analysis progress, inspect vulnerabilities, provide "False Positive" feedback, and download reports.
- **[NEW]** `notebooks/demo_pipeline.ipynb`: A Jupyter Notebook demonstrating the end-to-end pipeline and showing the effect of episodic memory.

## Verification Plan

### Automated Tests
- Run `scripts/build_index.py` with sample corpus files to verify ChromaDB ingestion.
- Run `scripts/evaluate_rag.py` to get RAGAS scores.
- Run `scripts/test_parser.py` and `scripts/test_retrieval.py` on small sample code fragments.

### Manual Verification
- Start the application with `docker compose up` and run a full pipeline on a sample repository using the Streamlit UI.
- Flag a finding as a "False Positive" and re-run the pipeline to verify that the `Self-Improving Feedback Agent` adjusts the result based on episodic memory.
