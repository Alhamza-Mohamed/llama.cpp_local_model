LLM API with FastAPI and llama.cpp

1- Overview

This project implements a simple backend API using FastAPI to interact with a local Large Language Model (LLM) powered by llama.cpp.

It supports:

Single-prompt text generation with control over key model parameters (max tokens, temperature, top-p).

Multi-turn chat conversations with server-side system message injection, allowing clients to send only user messages while preserving consistent model behavior.

The goal of this project is to practice clean backend architecture and proper separation of concerns when building LLM-powered APIs.



2- Features

Chat endpoint
Supports multi-turn conversations using role-based messages.

Generate endpoint
Supports single-prompt generation with configurable model parameters.

System message injection
Ensures consistent assistant behavior without exposing system prompts to the client.

Schema-based validation
Uses Pydantic models to validate requests and structure responses.



3- Project Structure
app/
├── main.py                # FastAPI entry point
├── core/
│   └── config.py          # Configuration (llama.cpp server URL)
├── models/
│   └── schemas.py         # Request and response schemas
├── services/
│   └── llama_service.py   # Prompt building and LLM communication logic
└── routes/
│   └── chat.py            # Chat endpoint
│   └── generate.py        # Single-prompt generation endpoint
├──rag_core/
	├── document.py        # Document class
	├── loader.py          # Load text files
	├── chunker.py         # Chunk documents
	├── embedder.py        # Embedding logic (open-source model)
	├── vector_store.py    # Simple in-memory store
	├── retriever.py       # Cosine similarity search
	├── prompt.py          # RAG prompt builder
	└── pipeline.py        # Orchestrates retrieval + LLM call


4- Installation & Setup

Prerequisites:
-Python 3.10+
-A local build of llama.cpp


Steps:

1.Install and build llama.cpp on your local machine.

2.Clone this repository.

3.Create a virtual environment: python -m venv venv

4.Activate the virtual environment: Linux / Mac: source venv/bin/activate Windows: venv\Scripts\activate

5.Install dependencies: pip install -r requirements.txt

6.Run the llama.cpp server (example): .\llama-server.exe -m smollm2-1.7b-instruct-q4_k_m.gguf --n-gpu-layers 99 --port 8081 
Make sure the server URL matches the value in core/config.py.

7.Run the FastAPI server: uvicorn main:app --host 127.0.0.1 --port 8000

8.Open the API documentation in your browser: http://127.0.0.1:8000/docs



5- Usage
Chat Example

Send a request to the /chat endpoint with user messages only:

{
  "messages": [
    { "role": "user", "content": "Hello, what are transformers?" }
  ]
}

The system message is injected automatically on the server side.


Notes

This project is intended for learning and experimentation.

Prompt formatting and system behavior are handled server-side to keep schemas simple and secure.

The architecture follows a clean separation between routing, schemas, services, and configuration.