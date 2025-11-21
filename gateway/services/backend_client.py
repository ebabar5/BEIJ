import httpx
import logging
from typing import Dict, Any, Optional
from fastapi import HTTPException

from config import settings

logger = logging.getLogger(__name__)

class BackendClient:
    """HTTP client for communicating with backend services"""
    
    def __init__(self):
        self.base_url = settings.BACKEND_URL
        self.timeout = settings.BACKEND_TIMEOUT
        self.client = None
    
    async def _get_client(self) -> httpx.AsyncClient:
        """Get or create HTTP client"""
        if self.client is None:
            self.client = httpx.AsyncClient(
                base_url=self.base_url,
                timeout=self.timeout,
                headers={
                    "User-Agent": "BEIJ-Gateway/1.0.0",
                    "Content-Type": "application/json"
                }
            )
        return self.client
    
    async def close(self):
        """Close HTTP client"""
        if self.client:
            await self.client.aclose()
            self.client = None
    
    async def get(self, endpoint: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Make GET request to backend"""
        try:
            client = await self._get_client()
            logger.info(f"GET {self.base_url}{endpoint}")
            
            response = await client.get(endpoint, params=params)
            response.raise_for_status()
            
            return response.json()
            
        except httpx.TimeoutException:
            logger.error(f"Timeout calling backend: {endpoint}")
            raise HTTPException(status_code=504, detail="Backend service timeout")
        except httpx.HTTPStatusError as e:
            logger.error(f"Backend HTTP error: {e.response.status_code} - {endpoint}")
            # Forward the backend error status and message
            try:
                error_detail = e.response.json()
            except:
                error_detail = {"message": "Backend service error"}
            raise HTTPException(status_code=e.response.status_code, detail=error_detail)
        except Exception as e:
            logger.error(f"Unexpected error calling backend: {e}")
            raise HTTPException(status_code=503, detail="Backend service unavailable")
    
    async def post(self, endpoint: str, data: Dict[str, Any], params: Optional[Dict] = None) -> Dict[str, Any]:
        """Make POST request to backend"""
        try:
            client = await self._get_client()
            logger.info(f"POST {self.base_url}{endpoint}")
            
            response = await client.post(endpoint, json=data, params=params)
            response.raise_for_status()
            
            return response.json()
            
        except httpx.TimeoutException:
            logger.error(f"Timeout calling backend: {endpoint}")
            raise HTTPException(status_code=504, detail="Backend service timeout")
        except httpx.HTTPStatusError as e:
            logger.error(f"Backend HTTP error: {e.response.status_code} - {endpoint}")
            try:
                error_detail = e.response.json()
            except:
                error_detail = {"message": "Backend service error"}
            raise HTTPException(status_code=e.response.status_code, detail=error_detail)
        except Exception as e:
            logger.error(f"Unexpected error calling backend: {e}")
            raise HTTPException(status_code=503, detail="Backend service unavailable")
    
    async def put(self, endpoint: str, data: Dict[str, Any], params: Optional[Dict] = None) -> Dict[str, Any]:
        """Make PUT request to backend"""
        try:
            client = await self._get_client()
            logger.info(f"PUT {self.base_url}{endpoint}")
            
            response = await client.put(endpoint, json=data, params=params)
            response.raise_for_status()
            
            return response.json()
            
        except httpx.TimeoutException:
            logger.error(f"Timeout calling backend: {endpoint}")
            raise HTTPException(status_code=504, detail="Backend service timeout")
        except httpx.HTTPStatusError as e:
            logger.error(f"Backend HTTP error: {e.response.status_code} - {endpoint}")
            try:
                error_detail = e.response.json()
            except:
                error_detail = {"message": "Backend service error"}
            raise HTTPException(status_code=e.response.status_code, detail=error_detail)
        except Exception as e:
            logger.error(f"Unexpected error calling backend: {e}")
            raise HTTPException(status_code=503, detail="Backend service unavailable")
    
    async def delete(self, endpoint: str, params: Optional[Dict] = None) -> Optional[Dict[str, Any]]:
        """Make DELETE request to backend"""
        try:
            client = await self._get_client()
            logger.info(f"DELETE {self.base_url}{endpoint}")
            
            response = await client.delete(endpoint, params=params)
            response.raise_for_status()
            
            # DELETE might return empty response
            if response.status_code == 204:
                return None
            
            try:
                return response.json()
            except:
                return None
                
        except httpx.TimeoutException:
            logger.error(f"Timeout calling backend: {endpoint}")
            raise HTTPException(status_code=504, detail="Backend service timeout")
        except httpx.HTTPStatusError as e:
            logger.error(f"Backend HTTP error: {e.response.status_code} - {endpoint}")
            try:
                error_detail = e.response.json()
            except:
                error_detail = {"message": "Backend service error"}
            raise HTTPException(status_code=e.response.status_code, detail=error_detail)
        except Exception as e:
            logger.error(f"Unexpected error calling backend: {e}")
            raise HTTPException(status_code=503, detail="Backend service unavailable")

# Global client instance
backend_client = BackendClient()
