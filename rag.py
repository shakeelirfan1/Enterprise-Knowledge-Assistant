import os
from dotenv import load_dotenv

from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

# Embedding Model
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Load Vector Database
db = FAISS.load_local(
    "vector_db",
    embeddings,
    allow_dangerous_deserialization=True
)

# Gemini LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.2
)


def ask_question(question):

    # Retrieve top 3 relevant chunks
    docs_with_scores = db.similarity_search_with_score(question, k=3)

    if len(docs_with_scores) == 0:
        return {
            "answer": "No relevant information found.",
            "sources": []
        }

    docs = [doc for doc, score in docs_with_scores]

    context = "\n\n".join(doc.page_content for doc in docs)

    prompt = f"""
You are an Enterprise Knowledge Assistant.

Rules:
1. Answer ONLY using the provided context.
2. Never make up information.
3. If the answer is missing, reply:
   "I could not find this information in the uploaded documents."
4. Keep answers concise and professional.
5. Use bullet points whenever appropriate.

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