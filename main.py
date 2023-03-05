from fastapi import FastAPI
from textgeneration import api as text_generation_api

app = FastAPI(title='AI utilty bot')

@app.get("/health")
def health():
    return {
        "message": "Server is healthy!"
    }

app.include_router(text_generation_api.router_v1)  