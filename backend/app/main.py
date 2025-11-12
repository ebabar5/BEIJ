from fastapi import FastAPI, HTTPException, Response
from app.routers.products import router as products_router
from app.routers.previews import router as preview_router
from app.routers.users_routes import router as users_router
from app.error_handling import register_errors

app = FastAPI()
register_errors(app)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/hello")
def hello():
    return {"msg": "Hello World"}

@app.get("/")
def home():
    return {"status": "ok"}

@app.get("/favicon.ico", include_in_schema=False)
def favicon():
    return Response(status_code=204)

app.include_router(products_router)
app.include_router(preview_router)
app.include_router(users_router)

def catch_all(_full_path: str):
    raise HTTPException(status_code=404)
