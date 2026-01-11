import streamlit as st
from src.utils import get_llm
from langchain_core.prompts import PromptTemplate

st.set_page_config(page_title="Tender Drafting", page_icon="📝")

st.header("📝 Smart Tender Document Generator")

# --- Inputs ---
col1, col2 = st.columns(2)
with col1:
    project_name = st.text_input("Project Name", "Corporate Office Renovation")
    budget = st.text_input("Estimated Budget", "$500,000")
with col2:
    timeline = st.text_input("Timeline", "6 Months")
    contract_type = st.selectbox("Contract Type", ["Fixed Price", "Time & Material", "Cost Plus"])

requirements = st.text_area("Key Technical Requirements", 
    "Need to replace all HVAC systems, install new LED lighting, and repaint 3 floors. "
    "Work must be done on weekends to avoid disrupting employees.")

# --- Logic ---
if st.button("Generate RFP Document"):
    if not requirements:
        st.warning("Please enter requirements.")
    else:
        with st.spinner("Drafting professional Tender Document..."):
            try:
                llm = get_llm()
                
                # We tell the AI to act as a Procurement Expert
                template = """
                You are a Senior Procurement Manager. Draft a structured Tender Request for Proposal (RFP) 
                for the following project:
                
                Project: {project_name}
                Budget: {budget}
                Timeline: {timeline}
                Type: {contract_type}
                
                Key Requirements:
                {requirements}
                
                Generate a professional document with these sections:
                1. Project Scope
                2. Technical Specifications (Expanded based on requirements)
                3. Vendor Eligibility Criteria
                4. Commercial Terms
                5. Evaluation Criteria
                
                Output Format: Markdown.
                """
                
                prompt = PromptTemplate.from_template(template)
                chain = prompt | llm
                
                response = chain.invoke({
                    "project_name": project_name, 
                    "budget": budget,
                    "timeline": timeline,
                    "contract_type": contract_type,
                    "requirements": requirements
                })
                
                # --- Output ---
                st.subheader("Generated Tender Document")
                st.markdown(response.content)
                
                # Download Button
                st.download_button(
                    label="Download RFP as Text",
                    data=response.content,
                    file_name=f"{project_name}_RFP.md",
                    mime="text/markdown"
                )
                
            except Exception as e:
                st.error(f"Error: {e}")