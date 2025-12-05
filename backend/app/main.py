from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.error_handling import register_errors
from app.routers import products_router, users_router, previews_router

app = FastAPI(
    title="BEIJ E-commerce API",
    description="Centralized API with all routes in main.py",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    # allow any origin in dev (works with our Docker setup)
    allow_origin_regex=".*",
    allow_credentials=False,      # no cookies-based auth, simple token/json is fine
    allow_methods=["*"],
    allow_headers=["*"],
)

register_errors(app)

@app.get("/")
def home():
    return {"status": "ok", "message": "BEIJ E-commerce API", "docs": "/docs"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/hello")
def hello():
    return {"msg": "Hello World"}

app.include_router(products_router.router)
app.include_router(users_router.router)
app.include_router(previews_router.router)
