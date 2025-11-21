#!/usr/bin/env python3
"""
Convenience script to run the BEIJ API Gateway
"""

import uvicorn
from config import settings

if __name__ == "__main__":
    print("🚀 Starting BEIJ API Gateway...")
    print(f"📍 Gateway URL: http://{settings.GATEWAY_HOST}:{settings.GATEWAY_PORT}")
    print(f"🔗 Backend URL: {settings.BACKEND_URL}")
    print(f"📚 API Docs: http://{settings.GATEWAY_HOST}:{settings.GATEWAY_PORT}/docs")
    print(f"🌍 Environment: {settings.ENVIRONMENT}")
    print("-" * 50)
    
    uvicorn.run(
        "main:app",
        host=settings.GATEWAY_HOST,
        port=settings.GATEWAY_PORT,
        reload=settings.ENVIRONMENT == "development",
        log_level=settings.LOG_LEVEL.lower()
    )
