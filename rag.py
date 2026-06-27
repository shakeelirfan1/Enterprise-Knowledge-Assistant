import os
from dotenv import load_dotenv

from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI

# Load environment variables
load_dotenv()

# Read Gemini API Key
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if GOOGLE_API_KEY is None:
    raise ValueError("GOOGLE_API_KEY not found. Add it to Streamlit Secrets.")

# Embedding Model
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Load FAISS Vector Database
db = FAISS.load_local(
    "vector_db",
    embeddings,
    allow_dangerous_deserialization=True
)

# Gemini LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    google_api_key=GOOGLE_API_KEY,
    temperature=0.2
)


def ask_question(question):
    """
    Search the vector database and answer using Gemini.
    """

    docs_with_scores = db.similarity_search_with_score(
        question,
        k=3
    )

    if not docs_with_scores:
        return {
            "answer": "No relevant information found.",
            "sources": []
        }

    docs = [doc for doc, score in docs_with_scores]

    context = "\n\n".join(
        doc.page_content for doc in docs
    )

    prompt = f"""
You are an Enterprise Knowledge Assistant.

Rules:
- Answer ONLY from the provided context.
- Never make up information.
- If the answer is unavailable, reply:
"I could not find this information in the uploaded documents."
- Keep answers concise.
- Use bullet points when appropriate.

Context:
{context}

Question:
{question}

Answer:
"""

    response = llm.invoke(prompt)

    return {
        "answer": response.content.strip(),
        "sources": docs
    }