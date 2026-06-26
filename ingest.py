import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

# Load PDFs
folder_path = "documents"
documents = []

for file in os.listdir(folder_path):
    if file.endswith(".pdf"):
        print(f"Loading {file}...")
        loader = PyPDFLoader(os.path.join(folder_path, file))
        documents.extend(loader.load())

# Split into chunks
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100
)

chunks = splitter.split_documents(documents)

print(f"\nTotal Chunks: {len(chunks)}")

print("\nCreating embeddings...")

# Create embeddings using Sentence Transformers
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Create FAISS vector database
vector_store = FAISS.from_documents(chunks, embeddings)

# Save the vector database
vector_store.save_local("vector_db")

print("\n✅ Vector Database Created Successfully!")