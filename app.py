import streamlit as st
import os
import tempfile
import chromadb
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from streamlit.runtime.uploaded_file_manager import UploadedFile
import requests
import json
import ollama  # ✅ Added missing import

# Ollama Embedding Function
class OllamaEmbeddingFunction:
    def __init__(self, url="http://localhost:11434/api/embeddings", model_name="nomic-embed-text:latest"):
        self.url = url
        self.model_name = model_name

    def __call__(self, input: list[str]) -> list[list[float]]:
        embeddings = []
        for text in input:
            payload = {"model": self.model_name, "prompt": text}
            response = requests.post(self.url, headers={"Content-Type": "application/json"}, data=json.dumps(payload))
            if response.status_code == 200:
                embeddings.append(response.json()["embedding"])
            else:
                raise Exception(f"Error calling Ollama API: {response.status_code}, {response.text}")
        return embeddings

# Process PDF Document
def process_document(uploaded_file: UploadedFile) -> list[Document]:
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    temp_file.write(uploaded_file.read())
    temp_file.close()

    loader = PyMuPDFLoader(temp_file.name)
    docs = loader.load()
    os.unlink(temp_file.name)

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=400, chunk_overlap=100)
    return text_splitter.split_documents(docs)

# Get Vector Store Collection
def get_vector_collection() -> chromadb.Collection:
    ollama_ef = OllamaEmbeddingFunction()
    chroma_client = chromadb.PersistentClient(path="./demo-rag-chroma")
    return chroma_client.get_or_create_collection(
        name="rag_app", embedding_function=ollama_ef, metadata={"hnsw:space": "cosine"}
    )

# Add Data to Vector Store
def add_to_vector_collection(all_splits: list[Document], file_name: str):
    collection = get_vector_collection()
    documents, metadatas, ids = [], [], []

    for idx, split in enumerate(all_splits):
        documents.append(split.page_content)
        metadatas.append(split.metadata)
        ids.append(f"{file_name}_{idx}")

    collection.upsert(documents=documents, metadatas=metadatas, ids=ids)
    st.success("Data added to the vector store!")

# Query Vector Store
def query_collection(prompt: str, n_results: int = 10):
    collection = get_vector_collection()
    results = collection.query(query_texts=[prompt], n_results=n_results)
    return results

# Call Ollama LLM
def call_llm(context: str, prompt: str):
    system_prompt = "You are an AI assistant that answers questions based on provided context."

    response = ollama.chat(
        model="llama3.2:3b",  # ✅ Fixed model name syntax
        stream=True,
        messages=[
            {"role": "system", "content": system_prompt},  # ✅ Fixed missing comma
            {"role": "user", "content": f"Context: {context}\nQuestion: {prompt}"},  # ✅ Fixed missing comma
        ],
    )

    for chunk in response:
        if not chunk["done"]:
            yield chunk["message"]["content"]
        else:
            break

# Streamlit UI
st.set_page_config(page_title="RAG Question Answer")

with st.sidebar:
    st.header("RAG Question Answer")
    uploaded_file = st.file_uploader("** Upload PDF files for QnA **", type=["pdf"], accept_multiple_files=False)
    process = st.button("Process")

if __name__ == "__main__":
    if uploaded_file and process:
        normalized_file_name = uploaded_file.name.translate(str.maketrans("-_. ", "____"))
        all_splits = process_document(uploaded_file)
        add_to_vector_collection(all_splits, normalized_file_name)

    st.header("RAG QUESTION ANSWER")
    prompt = st.text_area("**Ask a question related to your document:**")
    ask = st.button("ASK")

    if ask and prompt:
        results = query_collection(prompt)

        # ✅ Ensure that we have valid results before calling LLM
        documents = results.get("documents", [])
        if documents:
            context = documents[0]
            response = call_llm(context=context, prompt=prompt)
            st.write_stream(response)
        else:
            st.warning("No relevant information found in the document.")
