from fastapi import APIRouter, Request
from pydantic import  BaseModel

"""
API router: mini "router" object that groups related endpoints, it is like a chapter in a book.
the main app can include multiple routers

Request: gives access to the raw HTTP request object

BaseModel: a Pydantic class that allow define the shape of incoming data and automatically validates it
"""

router = APIRouter() 

class RAGRequest(BaseModel):
    query:str
"""
Means whoever call this endpoint must send a JSON body with a field called query
If they send the wrong type or forget the field, FastAPI rejects the request automatically with a helpful error — no manual validation needed.

"""
@router.post("/rag") # This decorator registers the function below it as a POST handler at the path /rag. When someone sends a POST request to /rag, this function runs.
def rag_endpoint(req: RAGRequest, request: Request):
    pipeline = request.app.state.pipeline
    result = pipeline.run(req.query)
    return result

"""
- 'req: RAGRequest': 
- 'request: Request'
- 'pipeline.run(req.query)'
- 'return result'

"""