import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
import PyPDF2


# Load environment variables
load_dotenv()

def extract_text_from_pdf(uploaded_file):
    """Extracts text from a standard PDF file."""
    try:
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        return f"Error reading PDF: {e}"

def get_llm():
    """Returns the Gemini Pro model instance."""
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY not found in .env file")
    
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash", # Flash is faster/cheaper for POC
        temperature=0.3,
        google_api_key=api_key
    )
    return llm