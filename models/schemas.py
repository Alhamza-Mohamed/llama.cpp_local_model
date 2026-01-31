from pydantic import BaseModel

""" 
Purpose:
    Define what comes in
    Define what goes out
    No logic 

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


# -------------------------- Response schema --------------------------

# This defines what our API returns
# Example JSON:
# {
#   "response": "Hi! How can I help?"
# }
class GenerateResponse(BaseModel):
    response: str