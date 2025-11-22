import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from app.main import app

client = TestClient(app)


class TestAdminLogin:
    """Test admin login functionality"""
    
    @patch('app.services.user_service.load_all')
    @patch('app.services.token_service.add_token')
    def test_admin_login_success_with_username(self, mock_add_token, mock_load):
    
        mock_load.return_value = [
            {
                "user_id": "admin-user-id",
                "username": "adminuser",
                "email": "admin@example.com",
                "hashed_password": "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYqJqZ5q5qW",
                "is_admin": True
            }
        ]
        
        with patch('app.services.user_service.verify_password', return_value=True):
            response = client.post(
                "/api/v1/users/admin/login",
                json={
                    "username_or_email": "adminuser",
                    "password": "password123",
                    "remember_me": False
                }
            )
        
        assert response.status_code == 200
        data = response.json()
        assert "user" in data
        assert "token" in data
        assert "expires_in" in data
        assert data["user"]["username"] == "adminuser"
        assert data["user"]["email"] == "admin@example.com"
        assert data["user"]["is_admin"] is True
        assert data["user"]["user_id"] == "admin-user-id"
        assert isinstance(data["token"], str)
        assert len(data["token"]) > 0
    
    @patch('app.services.user_service.load_all')
    @patch('app.services.token_service.add_token')
    def test_admin_login_success_with_email(self, mock_add_token, mock_load):
       
        mock_load.return_value = [
            {
                "user_id": "admin-user-id",
                "username": "adminuser",
                "email": "admin@example.com",
                "hashed_password": "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYqJqZ5q5qW",
                "is_admin": True
            }
        ]
        
        with patch('app.services.user_service.verify_password', return_value=True):
            response = client.post(
                "/api/v1/users/admin/login",
                json={
                    "username_or_email": "admin@example.com",
                    "password": "password123",
                    "remember_me": False
                }
            )
        
        assert response.status_code == 200
        data = response.json()
        assert "user" in data
        assert "token" in data
        assert data["user"]["email"] == "admin@example.com"
        assert data["user"]["is_admin"] is True
    
    @patch('app.services.user_service.load_all')
    def test_admin_login_failure_non_admin_user(self, mock_load):
        mock_load.return_value = [
            {
                "user_id": "regular-user-id",
                "username": "regularuser",
                "email": "regular@example.com",
                "hashed_password": "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYqJqZ5q5qW",
                "is_admin": False
            }
        ]
        
        with patch('app.services.user_service.verify_password', return_value=True):
            response = client.post(
                "/api/v1/users/admin/login",
                json={
                    "username_or_email": "regularuser",
                    "password": "password123",
                    "remember_me": False
                }
            )
        
        assert response.status_code == 403
        assert "admin access required" in response.json()["message"].lower()
    
    @patch('app.services.user_service.load_all')
    def test_admin_login_failure_wrong_password(self, mock_load):
        mock_load.return_value = [
            {
                "user_id": "admin-user-id",
                "username": "adminuser",
                "email": "admin@example.com",
                "hashed_password": "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYqJqZ5q5qW",
                "is_admin": True
            }
        ]
        
        with patch('app.services.user_service.verify_password', return_value=False):
            response = client.post(
                "/api/v1/users/admin/login",
                json={
                    "username_or_email": "adminuser",
                    "password": "wrongpassword",
                    "remember_me": False
                }
            )
        
        assert response.status_code == 401
        assert "invalid credentials" in response.json()["message"].lower()
    
    @patch('app.services.user_service.load_all')
    def test_admin_login_failure_nonexistent_user(self, mock_load):
        """Test admin login fails with non-existent user"""
        mock_load.return_value = []
        
        response = client.post(
            "/api/v1/users/admin/login",
            json={
                "username_or_email": "nonexistent",
                "password": "password123",
                "remember_me": False
            }
        )
        
        assert response.status_code == 401
        assert "invalid credentials" in response.json()["message"].lower()
    
    @patch('app.services.user_service.load_all')
    @patch('app.services.token_service.add_token')
    def test_admin_login_token_includes_admin_flag(self, mock_add_token, mock_load):
        """Test that admin login token includes is_admin=True"""
        mock_load.return_value = [
            {
                "user_id": "admin-user-id",
                "username": "adminuser",
                "email": "admin@example.com",
                "hashed_password": "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYqJqZ5q5qW",
                "is_admin": True
            }
        ]
        
        with patch('app.services.user_service.verify_password', return_value=True):
            response = client.post(
                "/api/v1/users/admin/login",
                json={
                    "username_or_email": "adminuser",
                    "password": "password123",
                    "remember_me": False
                }
            )
        
        assert response.status_code == 200
        data = response.json()
        assert data["user"]["is_admin"] is True
    
    @patch('app.services.user_service.load_all')
    @patch('app.services.token_service.add_token')
    def test_admin_login_with_remember_me(self, mock_add_token, mock_load):
        """Test admin login with remember_me flag"""
        mock_load.return_value = [
            {
                "user_id": "admin-user-id",
                "username": "adminuser",
                "email": "admin@example.com",
                "hashed_password": "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYqJqZ5q5qW",
                "is_admin": True
            }
        ]
        
        with patch('app.services.user_service.verify_password', return_value=True):
            response = client.post(
                "/api/v1/users/admin/login",
                json={
                    "username_or_email": "adminuser",
                    "password": "password123",
                    "remember_me": True
                }
            )
        
        assert response.status_code == 200
        data = response.json()
        assert "token" in data
        assert "expires_in" in data
        assert data["user"]["is_admin"] is True
        assert data["expires_in"] > 0
    
    @patch('app.services.user_service.load_all')
    def test_admin_login_mixed_users_database(self, mock_load):
        """Test admin login works when database has both admin and regular users"""
        mock_load.return_value = [
            {
                "user_id": "regular-user-id",
                "username": "regularuser",
                "email": "regular@example.com",
                "hashed_password": "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYqJqZ5q5qW",
                "is_admin": False
            },
            {
                "user_id": "admin-user-id",
                "username": "adminuser",
                "email": "admin@example.com",
                "hashed_password": "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYqJqZ5q5qW",
                "is_admin": True
            }
        ]
        
        with patch('app.services.user_service.verify_password', return_value=True):
            regular_response = client.post(
                "/api/v1/users/admin/login",
                json={
                    "username_or_email": "regularuser",
                    "password": "password123",
                    "remember_me": False
                }
            )
            assert regular_response.status_code == 403
            
            admin_response = client.post(
                "/api/v1/users/admin/login",
                json={
                    "username_or_email": "adminuser",
                    "password": "password123",
                    "remember_me": False
                }
            )
            assert admin_response.status_code == 200
            assert admin_response.json()["user"]["is_admin"] is True

