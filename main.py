# main.py
from fastapi import FastAPI
from routes.Chat import router

app = FastAPI(title="LLM API")

app.include_router(router)
