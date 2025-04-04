# ingest.py
import os
from dotenv import load_dotenv
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

def ingest_pdf(pdf_path: str, save_path: str = "embeddings/index"):
    # Step 1: Load PDF
    loader = PyPDFLoader(pdf_path)
    pages = loader.load()
    print(f"Loaded {len(pages)} pages from {pdf_path}")

    # Step 2: Split text into chunks
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100,
    )
    chunks = splitter.split_documents(pages)
    print(f"Split into {len(chunks)} chunks.")

    # Step 3: Embed chunks
    embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
    vectorstore = FAISS.from_documents(chunks, embedding=embeddings)

    # Step 4: Save FAISS index
    vectorstore.save_local(save_path)
    print(f"Saved vector index to {save_path}")

if __name__ == "__main__":
    ingest_pdf("data/policy.pdf")  # Place your PDF inside the `data/` folder
