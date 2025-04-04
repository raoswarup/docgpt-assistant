# qa.py

import os
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

def load_qa_chain(index_path="embeddings/index"):
    embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
    vectorstore = FAISS.load_local(index_path, embeddings, allow_dangerous_deserialization=True)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

    qa_chain = RetrievalQA.from_chain_type(
        llm=ChatOpenAI(openai_api_key=openai_api_key, temperature=0),
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True
    )
    return qa_chain

# 🧠 Wrapper function for external use (e.g., Streamlit)
chain = None

def run_qa_chain(query, chain):
    vectorstore = FAISS.load_local(
        "embeddings/temp_index",
        OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY")),
        allow_dangerous_deserialization=True
    )
    docs = vectorstore.similarity_search(query, k=3)

    result = chain.invoke({"input_documents": docs, "query": query})
    answer = result["result"]
    return answer, docs


# Optional CLI interface
if __name__ == "__main__":
    print("Ask a question about your document (type 'exit' to quit):")
    while True:
        query = input("\n🧠 You: ")
        if query.lower() in ['exit', 'quit']:
            break
        response = chain(query)
        print("\n🤖 Answer:", response['result'])
