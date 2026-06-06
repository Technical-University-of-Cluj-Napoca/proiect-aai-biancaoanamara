# Agentic AI Code Review - Task List

- [/] 1. Configuration & Infrastructure
  - [ ] Initialize `d:\BIANCA` structure
  - [ ] Create `requirements.txt`
  - [ ] Create `.gitignore`
  - [ ] Create `.env.example`
  - [ ] Create `Dockerfile`
  - [ ] Create `docker-compose.yml`

- [ ] 2. Data Transfer Objects (DTOs)
  - [ ] Create `src/dtos.py` with Pydantic models and Enums

- [ ] 3. Tooling & Setup Scripts
  - [ ] Create `src/tools/repo_tools.py`
  - [ ] Create `src/tools/vector_tools.py`
  - [ ] Create `scripts/build_index.py`
  - [ ] Create `scripts/evaluate_rag.py`
  - [ ] Create `scripts/test_parser.py`
  - [ ] Create `scripts/test_retrieval.py`

- [ ] 4. Agents Implementation
  - [ ] Create `src/agents/__init__.py`
  - [ ] Create `src/agents/parser_agent.py`
  - [ ] Create `src/agents/security_agent.py`
  - [ ] Create `src/agents/quality_agent.py`
  - [ ] Create `src/agents/feedback_agent.py`
  - [ ] Create `src/agents/report_agent.py`

- [ ] 5. LangGraph Orchestration
  - [ ] Create `src/graph/__init__.py`
  - [ ] Create `src/graph/workflow.py`

- [ ] 6. User Interface & Demonstration
  - [ ] Create `src/app.py` (Streamlit)
  - [ ] Create `notebooks/demo_pipeline.ipynb`
  - [ ] Create `README.md`

- [ ] 7. Populate Security Corpus
  - [ ] Populate `corpus/cve/`
  - [ ] Populate `corpus/owasp/`
  - [ ] Populate `corpus/cwe/`
  - [ ] Populate `corpus/framework_docs/`
  - [ ] Populate `corpus/style_guides/`
