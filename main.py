# main.py
from fastapi import FastAPI
from api.routes import router

app = FastAPI(title="LLM API")

app.include_router(router)
