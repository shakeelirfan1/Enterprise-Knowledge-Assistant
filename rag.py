import os
from dotenv import load_dotenv

from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

db = FAISS.load_local(
    "vector_db",
    embeddings,
    allow_dangerous_deserialization=True
)

llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    google_api_key=GOOGLE_API_KEY,
    temperature=0.2
)


def ask_question(question):

    docs = db.similarity_search(question, k=3)

    if not docs:
        return {
            "answer": "I could not find this information in the uploaded documents.",
            "sources": []
        }

    context = "\n\n".join(doc.page_content for doc in docs)

    prompt = f"""
You are an Enterprise Knowledge Assistant.

Rules:
- Answer ONLY from the context.
- Never make up information.
- If unavailable, reply:
'I could not find this information in the uploaded documents.'

Context:
{context}

Question:
{question}

Answer:
"""

    response = llm.invoke(prompt)

    return {
        "answer": response.content,
        "sources": docs
    }