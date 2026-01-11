import streamlit as st
from src.utils import get_llm
from langchain_core.prompts import PromptTemplate

st.set_page_config(page_title="Negotiation & Award", page_icon="🤝", layout="wide")

st.header("🤝 Negotiation & Award Assistant")
st.markdown("Generate strategic negotiation scripts and formal award documentation.")

# --- Tabs for Workflow ---
tab1, tab2 = st.tabs(["🗣️ Negotiation Coach", "🏆 Award Formalization"])

# ==========================================
# TAB 1: NEGOTIATION COACH
# ==========================================
with tab1:
    st.subheader("Generate Negotiation Strategy")
    
    col1, col2 = st.columns(2)
    with col1:
        vendor_name = st.text_input("Target Vendor", "FastBuild Construction")
        current_price = st.text_input("Current Bid Price", "$480,000")
    with col2:
        target_price = st.text_input("Target Price (The Goal)", "$450,000")
        levers = st.multiselect("Negotiation Levers", 
            ["Competitor has lower price", "Volume discount promise", "Long-term partnership", "Payment terms adjustment"],
            default=["Competitor has lower price"]
        )
    
    pain_points = st.text_area("Specific Issues to Address", "Their timeline is 1 month longer than the competitor.")

    if st.button("Generate Negotiation Script"):
        with st.spinner("Drafting negotiation strategy..."):
            llm = get_llm()
            template = """
            You are a Senior Procurement Negotiator.
            Target Vendor: {vendor_name}
            Current Bid: {current_price}
            Our Target: {target_price}
            
            Key Issues to address: {pain_points}
            Leverage to use: {levers}
            
            Task:
            1. Draft a persuasive **Email** to the vendor initiated the negotiation. Tone: Professional but firm.
            2. Provide a **"Script for Call"** - Bullet points of exactly what to say during a phone call to handle objections.
            
            Output as Markdown.
            """
            prompt = PromptTemplate.from_template(template)
            chain = prompt | llm
            response = chain.invoke({
                "vendor_name": vendor_name,
                "current_price": current_price,
                "target_price": target_price,
                "pain_points": pain_points,
                "levers": ", ".join(levers)
            })
            
            st.markdown(response.content)

# ==========================================
# TAB 2: AWARD FORMALIZATION
# ==========================================
with tab2:
    st.subheader("Generate Award Documents")
    
    final_vendor = st.text_input("Winning Vendor", vendor_name)
    final_amt = st.text_input("Final Agreed Amount", "$460,000")
    project_title = st.text_input("Project Title", "Corporate Office Renovation")
    
    if st.button("Generate Award Letter & Justification"):
        with st.spinner("Generating legal documents..."):
            llm = get_llm()
            template = """
            You are a Contracts Administrator.
            Vendor: {final_vendor}
            Project: {project_title}
            Value: {final_amt}
            
            Task:
            1. Write a formal **Letter of Award (LOA)** to the vendor. Include placeholders for dates and signatures.
            2. Write a brief **Internal Award Justification Note** for the CEO explaining why this vendor was chosen (mentioning value for money).
            
            Output as Markdown.
            """
            prompt = PromptTemplate.from_template(template)
            chain = prompt | llm
            response = chain.invoke({
                "final_vendor": final_vendor,
                "project_title": project_title,
                "final_amt": final_amt
            })
            
            st.markdown(response.content)
            
            # Download Button
            st.download_button(
                label="Download Award Docs",
                data=response.content,
                file_name="Award_Package.md"
            )