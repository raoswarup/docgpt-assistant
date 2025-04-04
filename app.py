# app.py (Enhanced)

from langchain_community.vectorstores import FAISS
from langchain_text_splitters import CharacterTextSplitter
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain.document_loaders import PyPDFLoader
import pandas as pd

from qa import load_qa_chain, run_qa_chain
import streamlit as st
import os
from dotenv import load_dotenv

chain = None
qa_history = []
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

# Session state initialization
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.title("📄 DocGPT Assistant")

uploaded_files = st.file_uploader("Upload your PDFs", type="pdf", accept_multiple_files=True)

if uploaded_files:
    with st.spinner("Processing PDFs..."):
        all_chunks = []
        filenames = []

        for uploaded_file in uploaded_files:
            filename = uploaded_file.name
            filenames.append(filename)

            with open(f"temp_{filename}", "wb") as f:
                f.write(uploaded_file.read())

            loader = PyPDFLoader(f"temp_{filename}")
            docs = loader.load()
            splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
            all_chunks.extend(splitter.split_documents(docs))

        # Create new index and vectorstore
        embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
        vectorstore = FAISS.from_documents(all_chunks, embeddings)
        vectorstore.save_local("embeddings/temp_index")
        chain = load_qa_chain(index_path="embeddings/temp_index")

        st.success("All PDFs processed. Ask your question below 👇")

        # Sidebar file list
        st.sidebar.markdown("### 📁 Uploaded Files")
        for name in filenames:
            st.sidebar.write(f"✅ {name}")

# Ask question
if chain:
    user_question = st.text_input("Ask a question:")
    if user_question:
        with st.spinner("Searching..."):
            answer, docs = run_qa_chain(user_question, chain)
            qa_history.append({"question": user_question, "answer": answer})
            st.markdown(f"**Answer:** {answer}")

            # Add to history
            st.session_state.chat_history.append((user_question, answer))

            # Show source documents
            with st.expander("🔍 Sources"):
                for i, doc in enumerate(docs):
                    st.markdown(f"**Source {i+1}:**\n{doc.page_content[:500]}...")

# Chat history
if st.session_state.chat_history:
    st.markdown("### 💬 Chat History")
    for q, a in st.session_state.chat_history:
        st.markdown(f"**You:** {q}")
        st.markdown(f"**DocGPT:** {a}")
        st.markdown("---")

if qa_history:
    st.markdown("### 🗂️ Q&A History")
    for i, entry in enumerate(reversed(qa_history)):
        st.markdown(f"**Q{i+1}:** {entry['question']}")
        st.markdown(f"**A{i+1}:** {entry['answer']}")
        st.markdown("---")


if qa_history:
    df = pd.DataFrame(qa_history)
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Q&A History",
        data=csv,
        file_name='qa_history.csv',
        mime='text/csv',
    )