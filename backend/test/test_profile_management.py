import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from app.main import app

client = TestClient(app)


class TestProfileManagement:
    
    @patch('app.services.user_service.load_all')
    def test_get_user_profile_success(self, mock_load):
        mock_load.return_value = [
            {
                "user_id": "test-user-id",
                "username": "testuser",
                "email": "test@example.com",
                "hashed_password": "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYqJqZ5q5qW",
                "is_admin": False
            }
        ]
        
        response = client.get("/api/v1/users/test-user-id")
        
        assert response.status_code == 200
        data = response.json()
        assert data["user_id"] == "test-user-id"
        assert data["username"] == "testuser"
        assert data["email"] == "test@example.com"
        assert data["is_admin"] is False
        assert "hashed_password" not in data
    
    @patch('app.services.user_service.load_all')
    def test_get_user_profile_not_found(self, mock_load):
        mock_load.return_value = []
        
        response = client.get("/api/v1/users/nonexistent-id")
        
        assert response.status_code == 404
        assert "not found" in response.json()["message"].lower()
    
    @patch('app.services.user_service.load_all')
    def test_get_admin_profile_includes_admin_flag(self, mock_load):
        mock_load.return_value = [
            {
                "user_id": "admin-user-id",
                "username": "adminuser",
                "email": "admin@example.com",
                "hashed_password": "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYqJqZ5q5qW",
                "is_admin": True
            }
        ]
        
        response = client.get("/api/v1/users/admin-user-id")
        
        assert response.status_code == 200
        assert response.json()["is_admin"] is True
    
    @patch('app.services.user_service.load_all')
    @patch('app.services.user_service.save_all')
    def test_update_username_success(self, mock_save, mock_load):
        mock_load.return_value = [
            {
                "user_id": "test-user-id",
                "username": "oldusername",
                "email": "test@example.com",
                "hashed_password": "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYqJqZ5q5qW",
                "is_admin": False
            }
        ]
        
        response = client.put(
            "/api/v1/users/test-user-id",
            json={"username": "newusername"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == "newusername"
        assert data["email"] == "test@example.com"
        assert data["user_id"] == "test-user-id"
        mock_save.assert_called_once()
    
    @patch('app.services.user_service.load_all')
    @patch('app.services.user_service.save_all')
    def test_update_email_success(self, mock_save, mock_load):
        mock_load.return_value = [
            {
                "user_id": "test-user-id",
                "username": "testuser",
                "email": "old@example.com",
                "hashed_password": "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYqJqZ5q5qW",
                "is_admin": False
            }
        ]
        
        response = client.put(
            "/api/v1/users/test-user-id",
            json={"email": "new@example.com"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == "new@example.com"
        assert data["username"] == "testuser"
        mock_save.assert_called_once()
    
    @patch('app.services.user_service.load_all')
    @patch('app.services.user_service.save_all')
    def test_update_password_success(self, mock_save, mock_load):
        mock_load.return_value = [
            {
                "user_id": "test-user-id",
                "username": "testuser",
                "email": "test@example.com",
                "hashed_password": "$2b$12$oldhash",
                "is_admin": False
            }
        ]
        
        response = client.put(
            "/api/v1/users/test-user-id",
            json={"password": "newpassword123"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == "testuser"
        assert data["email"] == "test@example.com"
        
        saved_data = mock_save.call_args[0][0]
        updated_user = saved_data[0]
        assert updated_user["hashed_password"] != "newpassword123"
        assert updated_user["hashed_password"].startswith("$2b$")
    
    @patch('app.services.user_service.load_all')
    @patch('app.services.user_service.save_all')
    def test_update_multiple_fields_success(self, mock_save, mock_load):
        mock_load.return_value = [
            {
                "user_id": "test-user-id",
                "username": "oldusername",
                "email": "old@example.com",
                "hashed_password": "$2b$12$oldhash",
                "is_admin": False
            }
        ]
        
        response = client.put(
            "/api/v1/users/test-user-id",
            json={
                "username": "newusername",
                "email": "new@example.com",
                "password": "newpassword123"
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == "newusername"
        assert data["email"] == "new@example.com"
        mock_save.assert_called_once()
    
    @patch('app.services.user_service.load_all')
    def test_update_profile_not_found(self, mock_load):
        mock_load.return_value = []
        
        response = client.put(
            "/api/v1/users/nonexistent-id",
            json={"username": "newname"}
        )
        
        assert response.status_code == 404
        assert "not found" in response.json()["message"].lower()
    
    @patch('app.services.user_service.load_all')
    def test_update_username_duplicate(self, mock_load):
        mock_load.return_value = [
            {
                "user_id": "test-user-id",
                "username": "testuser",
                "email": "test@example.com",
                "hashed_password": "$2b$12$hash",
                "is_admin": False
            },
            {
                "user_id": "other-user-id",
                "username": "existinguser",
                "email": "other@example.com",
                "hashed_password": "$2b$12$hash",
                "is_admin": False
            }
        ]
        
        response = client.put(
            "/api/v1/users/test-user-id",
            json={"username": "existinguser"}
        )
        
        assert response.status_code == 409
        assert "username already exists" in response.json()["message"].lower()
    
    @patch('app.services.user_service.load_all')
    def test_update_email_duplicate(self, mock_load):
        mock_load.return_value = [
            {
                "user_id": "test-user-id",
                "username": "testuser",
                "email": "test@example.com",
                "hashed_password": "$2b$12$hash",
                "is_admin": False
            },
            {
                "user_id": "other-user-id",
                "username": "otheruser",
                "email": "existing@example.com",
                "hashed_password": "$2b$12$hash",
                "is_admin": False
            }
        ]
        
        response = client.put(
            "/api/v1/users/test-user-id",
            json={"email": "existing@example.com"}
        )
        
        assert response.status_code == 409
        assert "email already exists" in response.json()["message"].lower()
    
    @patch('app.services.user_service.load_all')
    @patch('app.services.user_service.save_all')
    def test_update_username_allows_same_username(self, mock_save, mock_load):
        mock_load.return_value = [
            {
                "user_id": "test-user-id",
                "username": "testuser",
                "email": "test@example.com",
                "hashed_password": "$2b$12$hash",
                "is_admin": False
            }
        ]
        
        response = client.put(
            "/api/v1/users/test-user-id",
            json={"username": "testuser"}
        )
        
        assert response.status_code == 200
        assert response.json()["username"] == "testuser"
    
    @patch('app.services.user_service.load_all')
    @patch('app.services.user_service.save_all')
    def test_update_username_trimmed(self, mock_save, mock_load):
        mock_load.return_value = [
            {
                "user_id": "test-user-id",
                "username": "testuser",
                "email": "test@example.com",
                "hashed_password": "$2b$12$hash",
                "is_admin": False
            }
        ]
        
        response = client.put(
            "/api/v1/users/test-user-id",
            json={"username": "  newusername  "}
        )
        
        assert response.status_code == 200
        assert response.json()["username"] == "newusername"
        
        saved_data = mock_save.call_args[0][0]
        assert saved_data[0]["username"] == "newusername"
    
    @patch('app.services.user_service.load_all')
    @patch('app.services.user_service.save_all')
    def test_update_empty_payload_no_changes(self, mock_save, mock_load):
        mock_load.return_value = [
            {
                "user_id": "test-user-id",
                "username": "testuser",
                "email": "test@example.com",
                "hashed_password": "$2b$12$hash",
                "is_admin": False
            }
        ]
        
        response = client.put(
            "/api/v1/users/test-user-id",
            json={}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == "testuser"
        assert data["email"] == "test@example.com"
        mock_save.assert_called_once()
