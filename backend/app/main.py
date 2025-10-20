from fastapi import FastAPI
from app.routers.items import router as items_router

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/hello")
def hello():
    return {"msg": "Hello World"}

app.include_router(items_router)
