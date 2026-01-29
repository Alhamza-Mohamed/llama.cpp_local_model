from fastapi import FastAPI

# Pydantic is used by FastAPI to validate request/response schemas
from pydantic import BaseModel

# requests is used to call llama.cpp over HTTP
import requests
# Create the FastAPI application
app = FastAPI()


# This defines what the client must send to /generate
# Example JSON:
# {
#   "prompt": "Hello"
# }
class GenerateReqauest(BaseModel):
    prompt: str


# ----------- Response schema -----------

# This defines what our API returns
# Example JSON:
# {
#   "response": "Hi! How can I help?"
# }
class GenerateResponse(BaseModel):
    response: str

"""@app.get("/health")
def health():
    return {"status": "ok"}
"""


# ----------- llama.cpp server endpoint -----------

# This is where llama-server.exe is listening
# /completion is the default llama.cpp text generation endpoint
LLAMA_SERVER_URL = "http://127.0.0.1:8081/completion"


# ----------- API endpoint -----------

@app.post("/generate", response_model = GenerateResponse)
def generate (req: GenerateReqauest):
    """
    This function is called when:
    POST /generate
    """
    # This is the payload expected by llama.cpp
    # Minimal fields only     
    payload = {
         "prompt": req.prompt,  # user prompt
         "n_predict": 50,      # max tokens to generate
         "temperature": 0.7     # randomness

    }

    # send POST request to llama.cpp server
    r = requests.post(LLAMA_SERVER_URL, json = payload)

    # If llama.cpp returns 4xx / 5xx, raise an error immediately
    r.raise_for_status()

    data = r.json()

    # llama.cpp returns generated text under "content"
    return GenerateResponse(response = data["content"])