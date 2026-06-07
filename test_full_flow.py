"""
test_full_flow.py — Testul de integrare ("proba de foc")

Rulează cu:
    uv run python test_full_flow.py
sau:
    python test_full_flow.py
"""

from src.graph.workflow import WorkflowState, create_workflow

def main():
    # 1. Inițializăm workflow-ul compilat (LangGraph)
    print("=" * 60)
    print("  Security & Quality Analysis — Integration Test")
    print("=" * 60)

    app = create_workflow()

    # 2. Stare de test: cod cu SQL Injection clasic
    test_state: WorkflowState = {
        "repo_url": "local://test",
        "repo_path": "",
        "repository": None,   # va fi populat de clone_and_parse_node
        "reviews": [],
        "final_report": "",
    }

    # Notă: pentru testul local fără Git, putem testa direct agenții individuali
    # fără să trecem prin clone_and_parse (care necesită un URL real).
    # Varianta completă (cu URL real) e comentată mai jos.

    # ------------------------------------------------------------------ #
    #  Test rapid: agenții de securitate + calitate + feedback + raport    #
    # ------------------------------------------------------------------ #
    from src.dtos import FileReviewDTO, RepositoryDTO, CodeFileDTO
    from src.agents.security_agent import scan_file_for_vulnerabilities
    from src.agents.quality_agent import analyze_quality
    from src.agents.feedback_agent import apply_feedback_memory
    from src.agents.report_agent import generate_report

    # Codul vulnerabil de test
    test_file_path = "src/database.py"
    test_content = (
        "import sqlite3\n"
        "conn = sqlite3.connect('app.db')\n"
        "cursor = conn.cursor()\n\n"
        "def get_user(user_id):\n"
        "    # SQL Injection vulnerability!\n"
        "    cursor.execute('SELECT * FROM users WHERE id = ' + user_id)\n"
        "    return cursor.fetchone()\n\n"
        "def very_long_function_that_does_too_many_things(a, b, c, d, e):\n"
        "    # Code smell: too many parameters + long function\n"
        "    pass\n"
    )

    print(f"\n[1/4] Scanare securitate: {test_file_path}")
    review: FileReviewDTO = scan_file_for_vulnerabilities(test_file_path, test_content)

    print(f"[2/4] Analiză calitate cod")
    file_dto = CodeFileDTO(file_path=test_file_path, content=test_content)
    smells = analyze_quality(file_dto)
    review.code_smells = smells

    print(f"[3/4] Aplicare memorie episodică (feedback)")
    review = apply_feedback_memory(review)

    print(f"[4/4] Generare raport final")
    repo = RepositoryDTO(repo_url="local://test", files=[file_dto])
    report = generate_report(repo, [review])

    print("\n" + "=" * 60)
    print("  RAPORT FINAL")
    print("=" * 60)
    print(report)

    # ------------------------------------------------------------------ #
    #  Test complet cu URL Git real (decomentează pentru rulare reală)     #
    # ------------------------------------------------------------------ #
    # real_state: WorkflowState = {
    #     "repo_url": "https://github.com/user/repo",
    #     "repo_path": "",
    #     "repository": None,
    #     "reviews": [],
    #     "final_report": "",
    # }
    # result = app.invoke(real_state)
    # print(result["final_report"])


if __name__ == "__main__":
    main()