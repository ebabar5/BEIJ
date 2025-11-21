#!/usr/bin/env python3
"""
Convenience script to run the BEIJ API Gateway
"""

import uvicorn
import logging
from config import settings

if __name__ == "__main__":
    # Configure logging for startup messages
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    logger = logging.getLogger(__name__)
    
    logger.info("🚀 Starting BEIJ API Gateway...")
    logger.info(f"📍 Gateway URL: http://{settings.GATEWAY_HOST}:{settings.GATEWAY_PORT}")
    logger.info(f"🔗 Backend URL: {settings.BACKEND_URL}")
    logger.info(f"📚 API Docs: http://{settings.GATEWAY_HOST}:{settings.GATEWAY_PORT}/docs")
    logger.info(f"🌍 Environment: {settings.ENVIRONMENT}")
    logger.info("-" * 50)
    
    uvicorn.run(
        "main:app",
        host=settings.GATEWAY_HOST,
        port=settings.GATEWAY_PORT,
        reload=settings.ENVIRONMENT == "development",
        log_level=settings.LOG_LEVEL.lower()
    )
