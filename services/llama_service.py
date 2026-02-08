# requests is used to call llama.cpp over HTTP
import requests
from typing import List
from core.config import LLAMA_SERVER_URL
from models.schemas import GenerateRequest, chatRequest, ChatMessage

# -------------------- Prompt Builders --------------------

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


def build_chat_prompt(messages: List[ChatMessage]) -> str:
    """
    Build a chat-stile prompt from a list of messages.
    prepends role headrs (System, User, Assistant) for llama.cpp.
    """
    
    prompt = ""
    for message in messages:
            role_header = message.role.capitalize() # system -> System
            prompt += f"### {role_header}:\n{message.content}\n\n"
        
    # always continue as assistant
    prompt += "### Assistant:\n"
        
    return prompt

# -------------------- System Message Injection --------------------

DEFAULTE_SYSTEM_MESSAGE = "You are a helpful, concise AI assistant."

def inject_system_message(message: List [ChatMessage]) -> List[ChatMessage]:
    """
    Ensure a asystem message exists by injecting a default one
    at the beginnig of the conversation
    """
    system_message = ChatMessage(role="system",content=DEFAULTE_SYSTEM_MESSAGE)
    return [system_message,*message] # *message means unpack the list to append it in the [system_message,*message] list


# -------------------- LLM Communication --------------------

def generate_text(full_prompt: str ,req: GenerateRequest) -> str:
    """
    Send a formatted single-prompt to llama.cpp and return clean generated text.
    Used by /generate endpoint.
    """     

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
    data = response.json()

    # Extract generated text safely
    # Some llama.cpp builds return 'content', some 'completion'
    text = data.get("content") or data.get("completion") or ""

    # Strip leading/trailing whitespace and newlines for cleaner output
    return text.strip() #Removes extra newlines, leading/trailing spaces. Makes output nicer for clients

    

def generate_message(req: chatRequest, prompt:str) -> str:
    """
    Send a formatted chat prompt to llama.cpp and return generated text.
    Used by /chat endpoint.
    """
        
    payload = {
        "prompt": prompt ,
        "n_predict": req.n_predict,        # max tokens to generate
        "temperature": req.temperature,    # randomness (creativity vs stability)
        "top_p": req.top_p,                # nucleus sampling
        "stop": req.stop                   # stop when next section starts

     
    }

    response = requests.post(LLAMA_SERVER_URL, json=payload)
    response.raise_for_status()

    data = response.json()
    text = data.get("content") or data.get("completion") or ""
    return text.strip()


