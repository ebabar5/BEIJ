import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from app.main import app

client = TestClient(app)


class TestAccountSignInSignOut:
    
    @patch('app.services.user_service.load_all')
    @patch('app.repositories.token_repo.add_token')
    def test_login_success_with_username(self, mock_add_token, mock_load):
        mock_load.return_value = [
            {
                "user_id": "test-user-id",
                "username": "testuser",
                "email": "test@example.com",
                "hashed_password": "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYqJqZ5q5qW",
                "is_admin": False
            }
        ]
        
        with patch('app.services.user_service.verify_password', return_value=True):
            response = client.post(
                "/api/v1/users/login",
                json={
                    "username_or_email": "testuser",
                    "password": "password123",
                    "remember_me": False
                }
            )
        
        assert response.status_code == 200
        data = response.json()
        assert "user" in data
        assert "token" in data
        assert "expires_in" in data
        assert data["user"]["username"] == "testuser"
        assert data["user"]["email"] == "test@example.com"
        assert data["user"]["user_id"] == "test-user-id"
        assert isinstance(data["token"], str)
        assert len(data["token"]) > 0
    
    @patch('app.services.user_service.load_all')
    @patch('app.repositories.token_repo.add_token')
    def test_login_success_with_email(self, mock_add_token, mock_load):
        mock_load.return_value = [
            {
                "user_id": "test-user-id",
                "username": "testuser",
                "email": "test@example.com",
                "hashed_password": "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYqJqZ5q5qW",
                "is_admin": False
            }
        ]
        
        with patch('app.services.user_service.verify_password', return_value=True):
            response = client.post(
                "/api/v1/users/login",
                json={
                    "username_or_email": "test@example.com",
                    "password": "password123",
                    "remember_me": False
                }
            )
        
        assert response.status_code == 200
        data = response.json()
        assert "user" in data
        assert "token" in data
        assert data["user"]["email"] == "test@example.com"
    
    @patch('app.services.user_service.load_all')
    def test_login_failure_wrong_password(self, mock_load):
        mock_load.return_value = [
            {
                "user_id": "test-user-id",
                "username": "testuser",
                "email": "test@example.com",
                "hashed_password": "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYqJqZ5q5qW",
                "is_admin": False
            }
        ]
        
        with patch('app.services.user_service.verify_password', return_value=False):
            response = client.post(
                "/api/v1/users/login",
                json={
                    "username_or_email": "testuser",
                    "password": "wrongpassword",
                    "remember_me": False
                }
            )
        
        assert response.status_code == 401
        assert "invalid credentials" in response.json()["message"].lower()
    
    @patch('app.services.user_service.load_all')
    def test_login_failure_nonexistent_user(self, mock_load):
        mock_load.return_value = []
        
        response = client.post(
            "/api/v1/users/login",
            json={
                "username_or_email": "nonexistent",
                "password": "password123",
                "remember_me": False
            }
        )
        
        assert response.status_code == 401
        assert "invalid credentials" in response.json()["message"].lower()
    
    @patch('app.services.user_service.load_all')
    @patch('app.repositories.token_repo.add_token')
    @patch('app.routers.users_router.invalidate_token')
    def test_logout_success_with_token(self, mock_invalidate, mock_add_token, mock_load):
        mock_load.return_value = [
            {
                "user_id": "test-user-id",
                "username": "testuser",
                "email": "test@example.com",
                "hashed_password": "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYqJqZ5q5qW",
                "is_admin": False
            }
        ]
        
        with patch('app.services.user_service.verify_password', return_value=True):
            login_response = client.post(
                "/api/v1/users/login",
                json={
                    "username_or_email": "testuser",
                    "password": "password123",
                    "remember_me": False
                }
            )
        
        token = login_response.json()["token"]
        
        response = client.post(
            "/api/v1/users/logout",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == 200
        assert response.json() == {"message": "Logged out successfully"}
        mock_invalidate.assert_called_once()
    
    def test_logout_failure_without_token(self):
        response = client.post("/api/v1/users/logout")
        
        assert response.status_code == 401
        assert "authorization header required" in response.json()["message"].lower()
    
    @patch('app.routers.users_router.invalidate_token')
    def test_logout_with_invalid_token(self, mock_invalidate):
        mock_invalidate.return_value = None
        
        response = client.post(
            "/api/v1/users/logout",
            headers={"Authorization": "Bearer invalid-token-12345"}
        )
        
        assert response.status_code == 200
        mock_invalidate.assert_called_once_with("invalid-token-12345")
    
    @patch('app.services.user_service.load_all')
    @patch('app.repositories.token_repo.add_token')
    def test_login_with_remember_me(self, mock_add_token, mock_load):
        mock_load.return_value = [
            {
                "user_id": "test-user-id",
                "username": "testuser",
                "email": "test@example.com",
                "hashed_password": "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYqJqZ5q5qW",
                "is_admin": False
            }
        ]
        
        with patch('app.services.user_service.verify_password', return_value=True):
            response = client.post(
                "/api/v1/users/login",
                json={
                    "username_or_email": "testuser",
                    "password": "password123",
                    "remember_me": True
                }
            )
        
        assert response.status_code == 200
        data = response.json()
        assert "token" in data
        assert "expires_in" in data
        assert data["expires_in"] > 0
