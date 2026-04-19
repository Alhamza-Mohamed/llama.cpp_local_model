# Simple RAG API with FastAPI and llama.cpp (Local LLM)

## 1. Overview

This project implements a **Retrieval-Augmented Generation (RAG)** system using a FastAPI backend and a local Large Language Model (LLM) powered by llama.cpp.

The system retrieves relevant document chunks and uses them to generate context-aware answers through the LLM.

It supports:

* A **RAG endpoint** that retrieves answers grounded in user-provided documents, with similarity-based filtering to avoid out-of-context responses
* **Single-prompt generation** with control over key parameters (max tokens, temperature, top-p)
* **Multi-turn chat** with server-side system message injection for consistent behavior

The goal of this project is to **understand and implement RAG system components** while practicing **clean backend architecture** and **proper separation of concerns**.

---

## 2. RAG Pipeline

1. **Loading documents**
   Loads all `.txt` files from a directory and converts each file into a `Document` object.

2. **Chunking documents**
   Splits documents into chunks (~500 characters) using sentence-based splitting with overlap to preserve context.

3. **Embedding chunks**
   Converts each chunk into a vector representation using the `all-MiniLM-L6-v2` embedding model.
   *(A previous version used a simple hash-based embedder for learning purposes.)*

4. **Vector storing**
   Normalizes embeddings and stores them in memory (no external database).

5. **Retrieval**
   Computes similarity between the query embedding and stored vectors, returning the top-k most relevant chunks.

6. **Threshold filtering**
   Filters out low-similarity results to prevent generating answers when relevant context is missing.

7. **Prompt building**
   Combines retrieved chunks with the user query into a structured prompt.

8. **LLM generation**
   Sends the prompt to the local llama.cpp model to generate the final response.

---

## 3. Features

**RAG endpoint**
Retrieves relevant answers grounded in user-provided text documents.

**Similarity filtering**
Applies a similarity threshold to prevent out-of-context responses.

**Source attribution**
Returns metadata of the documents used to generate the answer.

**Chat endpoint**
Supports multi-turn conversations using role-based messages.

**Generate endpoint**
Supports single-prompt generation with configurable parameters.

**System message injection**
Ensures consistent assistant behavior without exposing system prompts.

**Schema-based validation**
Uses Pydantic models to validate requests and structure responses.

---

## 4. Project Structure

```
llama.cpp/
├── main.py                 # FastAPI entry point
├── core/
│   └── config.py           # Configuration (llama.cpp server URL)
├── models/
│   └── schemas.py          # Request and response schemas
├── services/
│   └── llama_service.py    # Low-level llama.cpp communication
├── routes/
│   ├── chat.py             # Chat endpoint
│   ├── generate.py         # Single prompt endpoint
│   └── rag.py              # RAG endpoint
├── rag_core/
│   ├── document.py         # Document abstraction
│   ├── loader.py           # Load text files
│   ├── chunker.py          # Chunk documents
│   ├── embedder.py         # Embedding module
│   ├── simple_embedder.py  # Legacy hash-based embedder (learning)
│   ├── vector_store.py     # In-memory vector store
│   ├── retriever.py        # Similarity-based retrieval
│   ├── prompt.py           # RAG prompt builder
│   ├── pipeline.py         # Pipeline orchestration
│   └── llm.py              # LLM adapter
├── rag_setup.py            # Build pipeline once at startup
├── data/                   # Input documents
```

---

## 5. Installation & Setup

### Prerequisites

* Python 3.11+
* Local build of llama.cpp

### Steps

1. Install and build llama.cpp
   *(See `llama_cpp_setup_guide.md`)*

2. Clone the repository

3. Create a virtual environment

   ```
   python -m venv venv
   ```

4. Activate the environment

   * Linux / Mac:

     ```
     source venv/bin/activate
     ```
   * Windows:

     ```
     venv\Scripts\activate
     ```

5. Install dependencies

   ```
   pip install -r requirements.txt
   ```

6. Run the llama.cpp server (example):

   ```
   .\llama-server.exe -m smollm2-1.7b-instruct-q4_k_m.gguf --n-gpu-layers 99 --port 8081
   ```

7. Ensure the server URL matches `core/config.py`

8. Run the FastAPI server

   ```
   uvicorn main:app --host 127.0.0.1 --port 8000
   ```

9. Open API documentation

   ```
   http://127.0.0.1:8000/docs
   ```

---

## 6. Usage

### Chat Example

Request to `/chat`:

```json
{
  "messages": [
    { "role": "user", "content": "Hello, what are transformers?" }
  ]
}
```

---

### RAG Example

Request to `/rag`:

**Query:**

```
tell me about machine learning
```

**Response:**

```json
{
  "answer": "...",
  "sources": [
    { "source": "...", "start": 0, "end": 120 }
  ]
}
```

---

### Out-of-scope Query

**Query:**

```
tell me about banana
```

**Response:**

```json
"I don't know"
```

---

## 7. Design Decisions

This section highlights key architectural and engineering decisions made in the project.

**In-memory vector store (no external database)**
The system stores embeddings directly in memory instead of using a vector database.
This keeps the architecture simple, transparent, and easier to debug, which is suitable for learning and experimentation.

**Sentence-based chunking with overlap**
Chunks are created using sentence boundaries with overlap between them.
This improves semantic continuity and avoids losing context at chunk borders.

**Similarity threshold filtering**
A threshold is applied to retrieved results before passing them to the LLM.
If no chunk meets the threshold, the system returns "I don't know" instead of generating potentially incorrect answers.

**External embedding model over custom embedder**
The project initially used a hash-based embedder for learning purposes.
It was later replaced with a pre-trained embedding model (`all-MiniLM-L6-v2`) to achieve better semantic representation and retrieval quality.

**Pipeline built once at startup**
The RAG pipeline (loading, chunking, embedding, storing) is executed once when the server starts.
This avoids recomputation on every request and significantly improves performance.

**Separation of concerns**
The system is structured into independent components (loader, chunker, embedder, retriever, prompt builder, LLM).
This makes the system modular, easier to debug, and easier to extend or replace individual parts.

**Server-side prompt construction**
All prompt logic is handled inside the backend.
This ensures consistent behavior and prevents clients from manipulating system-level instructions.

---
## Notes

* This project is intended for **learning and experimentation**
* Prompt formatting and system behavior are handled server-side
* The architecture follows **separation of concerns**
* Retrieval parameters (top_k, filtering, etc.) are controlled internally in the code
