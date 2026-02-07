from pydantic import BaseModel
from typing import List, Literal
""" 
Purpose:
    Define what comes in
    Define what goes out
    No logic 
    Schemas dont run code — they protect reality.
"""

# -------------------------- Request schema --------------------------
# This defines what the client must send to /generate
# Example JSON:
# {
#   "prompt": "Hello"
# }

class GenerateRequest(BaseModel):
    prompt: str                 # text the user wants the model to generate from
    n_predict: int = 256        # defult max tokens
    temperature: float = 0.7    # defult randomness
    top_p: float = 0.9          # nucleus sampling        
    stop: list[str] = ["###"]           #stop when next section starts

# -------------------------- Response schema --------------------------

# This defines what our API returns
# Example JSON:
# {
#   "response": "Hi! How can I help?"
# }

# --------------------------message schema------------------------------------

class ChatMessage (BaseModel):
    role: Literal["system", "user", "assistant"] # Literal means: role must be one of these exact strings, nothing else.
    content: str



class chatRequest(BaseModel):
    messages: List[ChatMessage] # List: messages is an ordered list of ChatMessage objects    
    n_predict: int = 256
    temperature: float = 0.7
    top_p:float = 0.9
    stop: list[str] = ["###"]

    model_config = {
        "json_schema_extra": {
            "example": {
                "messages": [
                    {
                        "role": "system",
                        "content": "you are a helpful AI assistant"
                    },
                    {
                        "role": "user",
                        "content": "hello, what is transformers?"
                    }
                ],                    
                "n_predict": 256,
                "temperature": 0.7,
                "top_p": 0.9,
                "stop": ["###"]
            }
        }
    }                        
       



class GenerateResponse(BaseModel):
    response: str