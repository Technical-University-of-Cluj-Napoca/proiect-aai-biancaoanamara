# Agentic AI Code Review and Security Vulnerability Detection System

This project is a multi-agent system built with LangGraph, LangChain, and Streamlit, designed to autonomously review GitHub repositories for security vulnerabilities and code quality issues.

## Features
- **Parser Agent**: Extracts codebase structure and functions using Python AST.
- **Security Agent**: Scans code for vulnerabilities using RAG (Retrieval-Augmented Generation) against CVE and OWASP corpuses.
- **Quality Agent**: Detects code smells and computes cyclomatic complexity using `radon`.
- **Self-Improving Feedback Agent**: Uses episodic memory via ChromaDB to remember user feedback on false positives.
- **Report Agent**: Aggregates findings into a detailed Markdown report.

## Setup Instructions

1. Clone this repository.
2. Ensure you have Docker installed, or run locally via `pip install -r requirements.txt`.
3. Create a `.env` file based on `.env.example` and add your `OPENAI_API_KEY`.
4. Run `python scripts/build_index.py` to index your security corpus (make sure to populate the `corpus/` folder first).
5. Run the Streamlit app: `streamlit run src/app.py` or use `docker-compose up`.

## Usage
- Open the Streamlit interface.
- Enter a GitHub repository URL.
- Click "Run Analysis".
- Review the generated Markdown report.
- If you spot a false positive, use the Feedback form at the bottom to mark it. The agent will remember this for future scans.
