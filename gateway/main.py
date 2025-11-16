from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
from contextlib import asynccontextmanager

from routers import products, users, previews
from services.backend_client import BackendClient
from config import settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize backend client
backend_client = BackendClient()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    logger.info("🚀 API Gateway starting up...")
    logger.info(f"Backend URL: {settings.BACKEND_URL}")
    yield
    logger.info("🛑 API Gateway shutting down...")
    await backend_client.close()

# Create FastAPI app
app = FastAPI(
    title="BEIJ API Gateway",
    description="Centralized API Gateway for BEIJ E-commerce Platform",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Health check endpoints
@app.get("/health")
async def health_check():
    """Gateway health check"""
    return {"status": "healthy", "service": "api-gateway"}

@app.get("/health/backend")
async def backend_health_check():
    """Check backend service health"""
    try:
        response = await backend_client.get("/health")
        return {"status": "healthy", "backend": response}
    except Exception as e:
        logger.error(f"Backend health check failed: {e}")
        raise HTTPException(status_code=503, detail="Backend service unavailable")

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": "Something went wrong in the gateway"
        }
    )

# Include routers with API prefix
app.include_router(products.router, prefix="/api/v1")
app.include_router(users.router, prefix="/api/v1") 
app.include_router(previews.router, prefix="/api/v1")

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "BEIJ API Gateway",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
