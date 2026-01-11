import streamlit as st
from src.utils import get_llm, extract_text_from_pdf
from langchain_core.prompts import PromptTemplate

st.set_page_config(page_title="Bid Comparison", page_icon="⚖️", layout="wide")

st.header("⚖️ Intelligent Bid Comparison")
st.markdown("Upload vendor proposals (PDF) to automatically extract and compare key metrics.")

# --- File Uploader ---
uploaded_files = st.file_uploader(
    "Upload Vendor Bids (PDF)", 
    type=["pdf"], 
    accept_multiple_files=True
)

if st.button("Analyze & Compare Bids"):
    if not uploaded_files:
        st.warning("Please upload at least one PDF file.")
    else:
        with st.spinner("Parsing documents and generating comparison Matrix..."):
            try:
                # 1. Extract Text from all PDFs
                combined_text = ""
                for file in uploaded_files:
                    text = extract_text_from_pdf(file)
                    combined_text += f"\n\n--- START OF BID FROM {file.name} ---\n{text}\n--- END OF BID ---\n"

                # 2. Setup the Analysis Prompt
                llm = get_llm()
                
                template = """
                You are a Senior Procurement Analyst. I have pasted the text from multiple vendor bids below.
                
                Your Task:
                1. Identify each vendor by name.
                2. Extract the following data points for each: Total Cost, Project Timeline, Payment Terms, Warranty Period, and any Key Exclusions/Deviations.
                3. Create a Comparison Table (Markdown format) to compare them side-by-side.
                4. Provide a "Recommendation" section: Which vendor offers the best value and why?
                5. List "Negotiation Levers": What specifically should we ask the preferred vendor to change?
                
                --- VENDOR DATA ---
                {vendor_data}
                """
                
                prompt = PromptTemplate.from_template(template)
                chain = prompt | llm
                
                # 3. Run the Chain
                response = chain.invoke({"vendor_data": combined_text})
                
                # 4. Display Results
                st.subheader("📊 Comparison Matrix")
                st.markdown(response.content)
                
            except Exception as e:
                st.error(f"An error occurred: {e}")

# --- Helper for Demo ---
with st.expander("ℹ️ How to test this?"):
    st.write("Since you might not have real vendor PDFs handy, create 2 simple PDFs with this content:")
    st.code("""
    [Vendor A - FastBuild Construction]
    Total Price: $480,000
    Timeline: 5 Months
    Payment: 50% Advance
    Exclusions: Does not include painting.
    
    [Vendor B - Quality Structurals]
    Total Price: $510,000
    Timeline: 6 Months
    Payment: Net 30 Days
    Includes: Full painting and cleaning.
    """)