# requests is used to call llama.cpp over HTTP
import requests

from core.config import LLAMA_SERVER_URL
from models.schemas import GenerateRequest

def build_prompt(user_prompt : str) -> str: #isolates prompt logic (clean separation)
    
    """
    Build an instuction-style prompt.
    This tells the model HOW to behaver
    """
    # ### Instruction: tells the model this is a task
    # ### Input: user message goes here
    # ### Response: The model will continue from here instead of rambling
    return f"""### Instruction: 
you are a helpful, concise AI assistant.

### Input:
{user_prompt}

### Response:     
"""
    
def generate_text(full_prompt: str ,req: GenerateRequest) -> str:
    # This is the payload expected by llama.cpp
    # Send a formatted prompt to llama.cpp and return clean output.
        
    

    payload = {
         "prompt": full_prompt,             # user prompt
         "n_predict": req.n_predict,        # max tokens to generate
         "temperature": req.temperature,    # randomness (creativity vs stability)
         "top_p": req.top_p,                # nucleus sampling
         "stop": req.stop                   # stop when next section starts

     
    }

    # send POST request to llama.cpp server
    response  = requests.post(LLAMA_SERVER_URL, json = payload ) #send as JSON POST

    # Raise error immediately if llama.cpp returns HTTP 4xx/5xx
    response .raise_for_status()

    # Parse JSON from llama.cpp
    data = response .json()

    # Extract generated text safely
    # Some llama.cpp builds return 'content', some 'completion'
    text = data.get("content") or data.get("completion") or ""

    # Strip leading/trailing whitespace and newlines for cleaner output
    return text.strip() #Removes extra newlines, leading/trailing spaces. Makes output nicer for clients

