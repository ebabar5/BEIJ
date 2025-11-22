

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from datetime import timedelta
from app.main import app

client = TestClient(app)


class TestRememberLogin:
    """Test remember_me login functionality"""
    
    @patch('app.services.user_service.load_all')
    @patch('app.repositories.token_repo.add_token')
    def test_login_with_remember_me_true_has_long_expiration(self, mock_add_token, mock_load):
        """Test that remember_me=True creates token with 30 day expiration"""
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
        assert "expires_in" in data
        
        expected_seconds = 30 * 24 * 60 * 60
        assert data["expires_in"] == expected_seconds
    
    @patch('app.services.user_service.load_all')
    @patch('app.repositories.token_repo.add_token')
    def test_login_with_remember_me_false_has_short_expiration(self, mock_add_token, mock_load):
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
        assert "expires_in" in data
        
        expected_seconds = 24 * 60 * 60
        assert data["expires_in"] == expected_seconds
    
    @patch('app.services.user_service.load_all')
    @patch('app.repositories.token_repo.add_token')
    def test_login_default_remember_me_is_false(self, mock_add_token, mock_load):
        """Test that remember_me defaults to False when not specified"""
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
                    "password": "password123"
                }
            )
        
        assert response.status_code == 200
        data = response.json()
        
       
        expected_seconds = 24 * 60 * 60
        assert data["expires_in"] == expected_seconds
    
    @patch('app.services.user_service.load_all')
    @patch('app.services.token_service.add_token')
    def test_remember_me_token_stored_with_flag(self, mock_add_token, mock_load):
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
        
        assert mock_add_token.called
        call_args = mock_add_token.call_args[0][0]
        assert call_args["remember_me"] is True
        assert "token" in call_args
        assert "user_id" in call_args
    
    @patch('app.services.user_service.load_all')
    @patch('app.services.token_service.add_token')
    def test_regular_token_stored_without_remember_me_flag(self, mock_add_token, mock_load):
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
        
        assert mock_add_token.called
        call_args = mock_add_token.call_args[0][0]
        assert call_args["remember_me"] is False
    
    @patch('app.services.user_service.load_all')
    @patch('app.repositories.token_repo.add_token')
    def test_remember_me_expiration_is_longer_than_regular(self, mock_add_token, mock_load):
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
            remember_me_response = client.post(
                "/api/v1/users/login",
                json={
                    "username_or_email": "testuser",
                    "password": "password123",
                    "remember_me": True
                }
            )
            
            regular_response = client.post(
                "/api/v1/users/login",
                json={
                    "username_or_email": "testuser",
                    "password": "password123",
                    "remember_me": False
                }
            )
        
        remember_me_data = remember_me_response.json()
        regular_data = regular_response.json()
        
        assert remember_me_data["expires_in"] > regular_data["expires_in"]
        assert remember_me_data["expires_in"] == regular_data["expires_in"] * 30

