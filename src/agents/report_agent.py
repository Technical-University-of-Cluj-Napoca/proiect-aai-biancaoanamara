from typing import List
from src.dtos import ReviewReportDTO, FileReviewDTO, RepositoryDTO

def generate_report(repo: RepositoryDTO, reviews: List[FileReviewDTO]) -> str:
    """Generates a markdown report summarizing the security and quality findings."""
    
    report = f"# Agentic Code Review Report\n\n"
    report += f"**Repository**: {repo.repo_url}\n"
    report += f"**Files Scanned**: {len(repo.files)}\n\n"
    
    report += "## Executive Summary\n"
    total_vulns = sum(len(r.vulnerabilities) for r in reviews)
    total_smells = sum(len(r.code_smells) for r in reviews)
    
    report += f"- Total Vulnerabilities: {total_vulns}\n"
    report += f"- Total Code Smells: {total_smells}\n\n"
    
    report += "## File Reviews\n\n"
    for review in reviews:
        if not review.vulnerabilities and not review.code_smells:
            continue
            
        report += f"### File: `{review.file_path}`\n"
        
        if review.vulnerabilities:
            report += "#### Security Vulnerabilities\n"
            for vuln in review.vulnerabilities:
                status = "*(False Positive)*" if vuln.false_positive else ""
                report += f"- **[{vuln.severity.value}]** {vuln.vulnerability_id} {status}\n"
                report += f"  - Description: {vuln.description}\n"
                if vuln.line_number:
                    report += f"  - Line: {vuln.line_number}\n"
                report += f"  - Remediation: {vuln.remediation}\n"
                
        if review.code_smells:
            report += "#### Code Smells\n"
            for smell in review.code_smells:
                report += f"- **[{smell.severity.value}]** {smell.smell_type}\n"
                report += f"  - {smell.description}\n"
                
        report += "\n---\n"
        
    return report
