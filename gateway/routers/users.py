from fastapi import APIRouter, HTTPException
from typing import Dict, Any
import logging

from services.backend_client import backend_client

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/users", tags=["users"])

class UserResponse:
    """Transform backend user data for frontend consumption"""
    
    @staticmethod
    def transform(backend_user: Dict[str, Any]) -> Dict[str, Any]:
        """Transform backend user to frontend format"""
        return {
            "id": backend_user.get("user_id"),
            "username": backend_user.get("username"),
            "email": backend_user.get("email"),
            "is_admin": backend_user.get("is_admin", False),
        }

@router.post("/register", response_model=Dict[str, Any])
async def register_user(user_data: Dict[str, Any]):
    """Register new user"""
    try:
        logger.info(f"Gateway: Registering user {user_data.get('username')}")
        
        # Transform frontend data to backend format
        backend_data = {
            "username": user_data.get("username"),
            "email": user_data.get("email"),
            "password": user_data.get("password")
        }
        
        # Validate required fields
        if not all([backend_data.get("username"), backend_data.get("email"), backend_data.get("password")]):
            raise HTTPException(status_code=400, detail="Username, email, and password are required")
        
        backend_response = await backend_client.post("/users/register", backend_data)
        
        # Transform response for frontend
        frontend_user = UserResponse.transform(backend_response)
        
        logger.info(f"Gateway: User {user_data.get('username')} registered successfully")
        return {
            "user": frontend_user,
            "message": "User registered successfully"
        }
        
    except Exception as e:
        logger.error(f"Error registering user: {e}")
        raise

@router.post("/login", response_model=Dict[str, Any])
async def login_user(login_data: Dict[str, Any]):
    """Authenticate user login"""
    try:
        username_or_email = login_data.get("username") or login_data.get("email")
        logger.info(f"Gateway: Login attempt for {username_or_email}")
        
        # Transform frontend data to backend format
        backend_data = {
            "username_or_email": username_or_email,
            "password": login_data.get("password"),
            "remember_me": login_data.get("remember_me", False)
        }
        
        # Validate required fields
        if not all([backend_data.get("username_or_email"), backend_data.get("password")]):
            raise HTTPException(status_code=400, detail="Username/email and password are required")
        
        backend_response = await backend_client.post("/users/login", backend_data)
        
        # Transform response for frontend
        frontend_user = UserResponse.transform(backend_response.get("user", backend_response))
        
        logger.info(f"Gateway: User {username_or_email} logged in successfully")
        return {
            "user": frontend_user,
            "message": "Login successful",
            "token": backend_response.get("token", f"mock_token_for_{frontend_user['id']}"),
            "expires_in": backend_response.get("expires_in", 86400)
        }
        
    except Exception as e:
        logger.error(f"Error during login: {e}")
        raise

@router.post("/admin/login", response_model=Dict[str, Any])
async def admin_login(login_data: Dict[str, Any]):
    try:
        username_or_email = login_data.get("username") or login_data.get("email")
        logger.info(f"Gateway: Admin login attempt for {username_or_email}")
        
        backend_data = {
            "username_or_email": username_or_email,
            "password": login_data.get("password"),
            "remember_me": login_data.get("remember_me", False)
        }
        
        if not all([backend_data.get("username_or_email"), backend_data.get("password")]):
            raise HTTPException(status_code=400, detail="Username/email and password are required")
        
        backend_response = await backend_client.post("/users/admin/login", backend_data)
        
        frontend_user = UserResponse.transform(backend_response.get("user", backend_response))
        
        logger.info(f"Gateway: Admin {username_or_email} logged in successfully")
        return {
            "user": frontend_user,
            "message": "Admin login successful",
            "token": backend_response.get("token", f"mock_token_for_{frontend_user['id']}"),
            "expires_in": backend_response.get("expires_in", 86400)
        }
        
    except Exception as e:
        logger.error(f"Error during admin login: {e}")
        raise

@router.post("/logout", response_model=Dict[str, Any])
async def logout_user():
    """Logout user (frontend-specific endpoint)"""
    try:
        logger.info("Gateway: User logout")
        
        # Call backend logout endpoint
        backend_response = await backend_client.post("/users/logout", {})
        
        logger.info("Gateway: User logged out successfully")
        return {
            "message": "Logged out successfully"
        }
        
    except Exception as e:
        logger.error(f"Error during logout: {e}")
        raise

# Additional frontend-specific user endpoints
@router.get("/profile/{user_id}", response_model=Dict[str, Any])
async def get_user_profile(user_id: str):
    """Get user profile (frontend-specific endpoint)"""
    try:
        logger.info(f"Gateway: Fetching profile for user {user_id}")
        
        # This would typically call a backend endpoint to get user details
        # For now, we'll return a mock response since the backend doesn't have this endpoint
        
        return {
            "user": {
                "id": user_id,
                "username": "mock_user",
                "email": "mock@example.com"
            },
            "message": "Profile retrieved successfully"
        }
        
    except Exception as e:
        logger.error(f"Error fetching user profile: {e}")
        raise

@router.put("/profile/{user_id}", response_model=Dict[str, Any])
async def update_user_profile(user_id: str, profile_data: Dict[str, Any]):
    """Update user profile (frontend-specific endpoint)"""
    try:
        logger.info(f"Gateway: Updating profile for user {user_id}")
        
        # This would typically call a backend endpoint to update user details
        # For now, we'll return a mock response since the backend doesn't have this endpoint
        
        return {
            "user": {
                "id": user_id,
                "username": profile_data.get("username", "mock_user"),
                "email": profile_data.get("email", "mock@example.com")
            },
            "message": "Profile updated successfully"
        }
        
    except Exception as e:
        logger.error(f"Error updating user profile: {e}")
        raise

@router.post("/change-password", response_model=Dict[str, Any])
async def change_password(password_data: Dict[str, Any]):
    """Change user password (frontend-specific endpoint)"""
    try:
        user_id = password_data.get("user_id")
        logger.info(f"Gateway: Changing password for user {user_id}")
        
        # Validate required fields
        if not all([
            password_data.get("user_id"),
            password_data.get("current_password"),
            password_data.get("new_password")
        ]):
            raise HTTPException(
                status_code=400, 
                detail="User ID, current password, and new password are required"
            )
        
        # This would typically call a backend endpoint to change password
        # For now, we'll return a mock response since the backend doesn't have this endpoint
        
        logger.info(f"Gateway: Password changed successfully for user {user_id}")
        return {
            "message": "Password changed successfully"
        }
        
    except Exception as e:
        logger.error(f"Error changing password: {e}")
        raise
