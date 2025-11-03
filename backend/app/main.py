from fastapi import FastAPI
from app.routers.products import router as products_router

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/hello")
def hello():
    return {"msg": "Hello World"}

app.include_router(products_router)
