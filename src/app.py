import streamlit as st
import sys
import os
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.graph.workflow import create_workflow
from src.agents.feedback_agent import save_feedback

load_dotenv()

st.set_page_config(page_title="Agentic Code Review", layout="wide")
st.title("Agentic AI Code Review & Vulnerability Detection")

repo_url = st.text_input("Enter GitHub Repository URL:")

if "report" not in st.session_state:
    st.session_state.report = None
if "reviews" not in st.session_state:
    st.session_state.reviews = None

if st.button("Run Analysis"):
    if repo_url:
        st.info("Initializing workflow...")
        workflow = create_workflow()
        
        initial_state = {
            "repo_url": repo_url,
            "repo_path": "",
            "repository": None,
            "reviews": [],
            "final_report": ""
        }
        
        with st.spinner("Running pipeline (Clone -> Parse -> Scan -> Report)..."):
            try:
                # We invoke the graph
                final_state = workflow.invoke(initial_state)
                st.session_state.report = final_state["final_report"]
                st.session_state.reviews = final_state["reviews"]
                st.success("Analysis Complete!")
            except Exception as e:
                st.error(f"Error during analysis: {e}")

if st.session_state.report:
    st.markdown("## Analysis Report")
    st.markdown(st.session_state.report)
    
    st.markdown("---")
    st.markdown("## Feedback / False Positives")
    st.write("If you noticed any false positives, you can flag them here so the agent learns for next time.")
    
    # Simple form to collect feedback
    with st.form("feedback_form"):
        # Gather all vuln IDs
        all_vulns = []
        for review in st.session_state.reviews:
            for vuln in review.vulnerabilities:
                all_vulns.append((vuln.vulnerability_id, review.file_path, vuln.description))
                
        if all_vulns:
            selected_vuln = st.selectbox("Select Vulnerability", [f"{v[0]} in {v[1]}" for v in all_vulns])
            comments = st.text_area("Why is this a false positive?")
            submitted = st.form_submit_button("Mark as False Positive")
            
            if submitted:
                # Parse selection
                vuln_id = selected_vuln.split(" in ")[0]
                file_path = selected_vuln.split(" in ")[1]
                
                save_feedback(vulnerability_id=vuln_id, file_path=file_path, status="FALSE_POSITIVE", comments=comments)
                st.success("Feedback saved to episodic memory! Future scans will flag this as a false positive.")
        else:
            st.write("No vulnerabilities found to provide feedback on.")
            st.form_submit_button("Submit", disabled=True)
