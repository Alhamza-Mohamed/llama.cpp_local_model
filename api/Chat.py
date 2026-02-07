from fastapi import APIRouter
from models.schemas import  chatRequest, GenerateResponse
from services.llama_service import build_prompt, generate_message, build_chat_prompt

router = APIRouter()

# -------------------------- API endpoint --------------------------

@router.post("/generate", response_model = GenerateResponse)
def generate (req: chatRequest):
    """
    This function is called when:
    POST /generate
    Automatically validates incoming JSON against GenerateRequest
    Automatically returns JSON formatted as GenerateResponse
    """
    
    message_prompt = build_chat_prompt(req.messages)
    result = generate_message( req, message_prompt)
    return GenerateResponse(response = result)