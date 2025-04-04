# 📄 DocGPT Assistant

DocGPT Assistant is an intelligent, multi-PDF document question-answering tool powered by OpenAI and LangChain. It enables users to upload internal documents (e.g., HR policies, SOPs, manuals), ask natural language questions, and get real-time answers with source references.

> ✅ Built with LangChain, FAISS, OpenAI, and Streamlit

---

## 🚀 Features

- 📁 Upload one or more PDF documents
- 🧠 Ask questions in natural language
- 🔍 Get accurate answers with referenced source chunks
- 💬 Chat history maintained throughout the session
- 📥 Download Q&A history as a CSV
- 🔐 Optional password protection for secure access

---

## 📸 Demo

![demo-screenshot](demo_screenshot.png) <!-- Optional: Add a real screenshot here -->

---

## 🧱 Tech Stack

- **Frontend:** Streamlit
- **Backend:** LangChain + OpenAI GPT (via API)
- **Vector Store:** FAISS
- **Embeddings:** OpenAI Embeddings API
- **PDF Processing:** PyPDFLoader

---

## 🛠️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/docgpt-assistant.git
cd docgpt-assistant
