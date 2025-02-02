Here's a sample `README.md` file for your GitHub repository that explains how to use the code, install dependencies, and run the application.

---

# RAG Question Answer System

This is a **RAG (Retriever-augmented Generation)** system built using Streamlit, Ollama's API for embeddings, and a vector store (Chroma) for document retrieval. The system allows users to upload PDF documents, store them in a vector store, and ask questions related to the content of these documents. The system retrieves relevant information from the documents and generates answers using a language model.

## Features

- **Document Upload**: Upload a PDF document and process its content for querying.
- **Vector Store Integration**: Uses Chroma to store the embeddings of documents and efficiently query them.
- **Query Answering**: Ask questions related to the document, and the system uses retrieval and generation to generate an answer.
- **Ollama API**: Uses Ollama's LLM to answer questions based on the provided context.

## Requirements

To run this project, you'll need the following dependencies:

- Python 3.7+
- Streamlit
- Requests
- Chroma
- LangChain
- Ollama (local LLM API)

### Install dependencies

To install the required Python libraries, use the following:

```bash
pip install streamlit requests chromadb langchain ollama
```

Make sure that you have the Ollama API running locally before using this system.

## Setup

### Ollama API
This system integrates with **Ollama's local LLM API** to process embeddings and generate answers. To set up Ollama:

1. Download and set up Ollama from [https://ollama.com/](https://ollama.com/).
2. Make sure the Ollama API is running locally on the default port `11434`. The system assumes the API will be available at `http://localhost:11434`.

### Running the Application

1. Clone the repository:

```bash
git clone https://github.com/yourusername/rag-question-answer-system.git
cd rag-question-answer-system
```

2. Run the Streamlit app:

```bash
streamlit run app.py
```

3. Once the app starts, you can:

- **Upload PDF**: Upload a PDF document for processing.
- **Ask Questions**: After the document is processed and stored, you can ask questions related to the document content.

### Functionality

1. **Uploading PDFs**: 
   - The uploaded PDF will be processed and split into smaller chunks (pages).
   - These chunks are embedded and stored in a Chroma vector store.

2. **Asking Questions**: 
   - After processing the document, you can ask any question related to the document. 
   - The system will search for the most relevant information from the document, pass it to the Ollama model, and generate a response.

## Code Explanation

### 1. **OllamaEmbeddingFunction**:
This class handles the embedding of input text using the Ollama model. The embeddings are returned and used for document storage and retrieval.

### 2. **process_document**:
This function processes the uploaded PDF document, loads the content, and splits it into smaller chunks using `RecursiveCharacterTextSplitter`.

### 3. **get_vector_collection**:
This function initializes a Chroma vector store and returns the collection where document embeddings are stored.

### 4. **add_to_vector_collection**:
This function adds the split documents' embeddings to the Chroma vector store.

### 5. **query_collection**:
This function queries the vector store for the most relevant documents based on the user's input query.

### 6. **call_llm**:
This function sends the relevant context (extracted from the query) to the Ollama API to generate a response. It handles the response and ensures the model's reply is correctly parsed and displayed.

### 7. **Streamlit UI**:
The UI is built using Streamlit. It allows users to upload PDFs, process them, and ask questions related to the document content. The results are displayed in the interface.

## Troubleshooting

### 1. **Error: Ollama API not found**
Make sure you have the Ollama API running locally on port `11434`. If you encounter connection errors, check that the Ollama service is up and running.

### 2. **Error: No relevant information found**
This error occurs when no relevant content is found in the vector store for the provided query. Ensure that the document was properly uploaded and processed before querying.

## Contributing

If you'd like to contribute to this project, feel free to fork the repository and submit a pull request. Any contributions to improve functionality, bug fixes, or feature additions are welcome!

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

### Notes:
1. Replace `https://github.com/yourusername/rag-question-answer-system.git` with your actual GitHub repository link.
2. Adjust `app.py` file name if needed (the Streamlit app file).
3. Ensure Ollama is correctly set up and running before testing.

Let me know if you need further adjustments!
