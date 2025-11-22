from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.error_handling import register_errors

# Import the routers
from app.routers import products_router, users_router, previews_router

app = FastAPI(
    title="BEIJ E-commerce API",
    description="Centralized API with all routes in main.py",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "http://localhost:8080",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

register_errors(app)

# Basic health check endpoints (kept in main.py as they're simple and universal)
@app.get("/")
def home():
    return {"status": "ok", "message": "BEIJ E-commerce API", "docs": "/docs"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/hello")
def hello():
    return {"msg": "Hello World"}

# Register all routers
# Each router handles a specific domain of the application
app.include_router(products_router.router)
app.include_router(users_router.router)
app.include_router(previews_router.router) 
