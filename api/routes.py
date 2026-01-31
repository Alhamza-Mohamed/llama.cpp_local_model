from fastapi import APIRouter
from models.schemas import GenerateRequest, GenerateResponse
from services.llama_service import generate_text

router = APIRouter()

# -------------------------- API endpoint --------------------------

@router.post("/generate", response_model = GenerateResponse)
def generate (req: GenerateRequest):
    """
    This function is called when:
    POST /generate
    Automatically validates incoming JSON against GenerateRequest
    Automatically returns JSON formatted as GenerateResponse
    """
    result = generate_text(req)
    return GenerateResponse(response = result)