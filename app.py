import streamlit as st

st.set_page_config(page_title="Tender.AI", page_icon="🏗️", layout="wide")

st.title("🏗️ Tender.AI: Intelligent Procurement Agent")

st.markdown("""
### Welcome to the Future of Procurement
This Agent assists specifically in the **Engineering & Construction** domain.

**Select a module from the sidebar to begin:**
1. **📝 Tender Drafting:** Generate full RFP documents from simple requirements.
2. **⚖️ Bid Comparison:** Upload vendor PDFs and get an auto-comparison table.
3. **🤝 Negotiation & Award:** Get AI-driven negotiation strategies and award letters.

---
*Powered by Google Gemini & LangChain*
""")