from fastapi import FastAPI
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

# register routers are all in one place 
routers = [products_router, preview_router, users_router]
for r in routers: 
    app.include_router(r) 
