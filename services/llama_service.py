# requests is used to call llama.cpp over HTTP
import requests

from core.config import LLAMA_SERVER_URL
from models.schemas import GenerateRequest

def generate_text(req: GenerateRequest) -> str:
    # This is the payload expected by llama.cpp
    # Minimal fields only     
    payload = {
         "prompt": req.prompt,              # user prompt
         "n_predict": req.n_predict,        # max tokens to generate
         "temperature": req.temperature     # randomness

    }

    # send POST request to llama.cpp server
    r = requests.post(LLAMA_SERVER_URL, json = payload ) #send as JSON POST

    # Raise error immediately if llama.cpp returns HTTP 4xx/5xx
    r.raise_for_status()

    # Parse JSON from llama.cpp
    data = r.json()

    # Extract generated text safely
    # Some llama.cpp builds return 'content', some 'completion'
    text = data.get("content") or data.get("completion") or ""

    # Strip leading/trailing whitespace and newlines for cleaner output
    return text.strip() #Removes extra newlines, leading/trailing spaces. Makes output nicer for clients