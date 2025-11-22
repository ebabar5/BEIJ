import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from app.main import app

client = TestClient(app)


class TestSavedItemsEndpoints:
    
    @patch('app.services.user_service.load_all')
    @patch('app.services.user_service.load_products')
    @patch('app.services.user_service.save_all')
    def test_save_item_success(self, mock_save, mock_load_products, mock_load_users):
        mock_load_users.return_value = [
            {
                "user_id": "test-user-id",
                "username": "testuser",
                "email": "test@example.com",
                "hashed_password": "$2b$12$hash",
                "is_admin": False,
                "saved_item_ids": []
            }
        ]
        mock_load_products.return_value = [
            {
                "product_id": "product-123",
                "product_name": "Test Product"
            }
        ]
        
        response = client.post("/api/v1/users/test-user-id/saved-items/product-123")
        
        assert response.status_code == 200
        data = response.json()
        assert data["user_id"] == "test-user-id"
        assert "product-123" in data["saved_item_ids"]
        mock_save.assert_called_once()
    
    @patch('app.services.user_service.load_all')
    @patch('app.services.user_service.load_products')
    @patch('app.services.user_service.save_all')
    def test_save_item_duplicate_not_added_twice(self, mock_save, mock_load_products, mock_load_users):
        mock_load_users.return_value = [
            {
                "user_id": "test-user-id",
                "username": "testuser",
                "email": "test@example.com",
                "hashed_password": "$2b$12$hash",
                "is_admin": False,
                "saved_item_ids": ["product-123"]
            }
        ]
        mock_load_products.return_value = [
            {
                "product_id": "product-123",
                "product_name": "Test Product"
            }
        ]
        
        response = client.post("/api/v1/users/test-user-id/saved-items/product-123")
        
        assert response.status_code == 200
        data = response.json()
        assert data["saved_item_ids"].count("product-123") == 1
        mock_save.assert_not_called()
    
    @patch('app.services.user_service.load_all')
    @patch('app.services.user_service.load_products')
    def test_save_item_user_not_found(self, mock_load_products, mock_load_users):
        mock_load_users.return_value = []
        mock_load_products.return_value = [
            {"product_id": "product-123", "product_name": "Test"}
        ]
        
        response = client.post("/api/v1/users/nonexistent-user/saved-items/product-123")
        
        assert response.status_code == 404
        assert "not found" in response.json()["message"].lower()
    
    @patch('app.services.user_service.load_all')
    @patch('app.services.user_service.load_products')
    def test_save_item_product_not_found(self, mock_load_products, mock_load_users):
        mock_load_users.return_value = [
            {
                "user_id": "test-user-id",
                "username": "testuser",
                "email": "test@example.com",
                "hashed_password": "$2b$12$hash",
                "is_admin": False,
                "saved_item_ids": []
            }
        ]
        mock_load_products.return_value = []
        
        response = client.post("/api/v1/users/test-user-id/saved-items/nonexistent-product")
        
        assert response.status_code == 404
        assert "not found" in response.json()["message"].lower()
    
    @patch('app.services.user_service.load_all')
    @patch('app.services.user_service.load_products')
    @patch('app.services.user_service.save_all')
    def test_save_multiple_items(self, mock_save, mock_load_products, mock_load_users):
        mock_load_users.return_value = [
            {
                "user_id": "test-user-id",
                "username": "testuser",
                "email": "test@example.com",
                "hashed_password": "$2b$12$hash",
                "is_admin": False,
                "saved_item_ids": []
            }
        ]
        mock_load_products.return_value = [
            {"product_id": "product-1", "product_name": "Product 1"},
            {"product_id": "product-2", "product_name": "Product 2"}
        ]
        
        response1 = client.post("/api/v1/users/test-user-id/saved-items/product-1")
        assert response1.status_code == 200
        assert "product-1" in response1.json()["saved_item_ids"]
        
        mock_load_users.return_value = [
            {
                "user_id": "test-user-id",
                "username": "testuser",
                "email": "test@example.com",
                "hashed_password": "$2b$12$hash",
                "is_admin": False,
                "saved_item_ids": ["product-1"]
            }
        ]
        
        response2 = client.post("/api/v1/users/test-user-id/saved-items/product-2")
        assert response2.status_code == 200
        assert "product-1" in response2.json()["saved_item_ids"]
        assert "product-2" in response2.json()["saved_item_ids"]
    
    @patch('app.services.user_service.load_all')
    def test_get_saved_items_success(self, mock_load_users):
        mock_load_users.return_value = [
            {
                "user_id": "test-user-id",
                "username": "testuser",
                "email": "test@example.com",
                "hashed_password": "$2b$12$hash",
                "is_admin": False,
                "saved_item_ids": ["product-1", "product-2", "product-3"]
            }
        ]
        
        response = client.get("/api/v1/users/test-user-id/saved-items")
        
        assert response.status_code == 200
        data = response.json()
        assert data["user_id"] == "test-user-id"
        assert data["saved_item_ids"] == ["product-1", "product-2", "product-3"]
    
    @patch('app.services.user_service.load_all')
    def test_get_saved_items_empty_list(self, mock_load_users):
        mock_load_users.return_value = [
            {
                "user_id": "test-user-id",
                "username": "testuser",
                "email": "test@example.com",
                "hashed_password": "$2b$12$hash",
                "is_admin": False,
                "saved_item_ids": []
            }
        ]
        
        response = client.get("/api/v1/users/test-user-id/saved-items")
        
        assert response.status_code == 200
        data = response.json()
        assert data["saved_item_ids"] == []
    
    @patch('app.services.user_service.load_all')
    def test_get_saved_items_user_not_found(self, mock_load_users):
        mock_load_users.return_value = []
        
        response = client.get("/api/v1/users/nonexistent-user/saved-items")
        
        assert response.status_code == 404
        assert "not found" in response.json()["message"].lower()
    
    @patch('app.services.user_service.load_all')
    @patch('app.services.user_service.save_all')
    def test_unsave_item_success(self, mock_save, mock_load_users):
        mock_load_users.return_value = [
            {
                "user_id": "test-user-id",
                "username": "testuser",
                "email": "test@example.com",
                "hashed_password": "$2b$12$hash",
                "is_admin": False,
                "saved_item_ids": ["product-1", "product-2", "product-3"]
            }
        ]
        
        response = client.delete("/api/v1/users/test-user-id/saved-items/product-2")
        
        assert response.status_code == 200
        data = response.json()
        assert data["user_id"] == "test-user-id"
        assert "product-2" not in data["saved_item_ids"]
        assert "product-1" in data["saved_item_ids"]
        assert "product-3" in data["saved_item_ids"]
        mock_save.assert_called_once()
    
    @patch('app.services.user_service.load_all')
    def test_unsave_item_not_in_list(self, mock_load_users):
        mock_load_users.return_value = [
            {
                "user_id": "test-user-id",
                "username": "testuser",
                "email": "test@example.com",
                "hashed_password": "$2b$12$hash",
                "is_admin": False,
                "saved_item_ids": ["product-1", "product-3"]
            }
        ]
        
        response = client.delete("/api/v1/users/test-user-id/saved-items/product-2")
        
        assert response.status_code == 200
        data = response.json()
        assert data["saved_item_ids"] == ["product-1", "product-3"]
    
    @patch('app.services.user_service.load_all')
    def test_unsave_item_user_not_found(self, mock_load_users):
        mock_load_users.return_value = []
        
        response = client.delete("/api/v1/users/nonexistent-user/saved-items/product-123")
        
        assert response.status_code == 404
        assert "not found" in response.json()["message"].lower()
    
    @patch('app.services.user_service.load_all')
    def test_unsave_item_product_not_in_list(self, mock_load_users):
        mock_load_users.return_value = [
            {
                "user_id": "test-user-id",
                "username": "testuser",
                "email": "test@example.com",
                "hashed_password": "$2b$12$hash",
                "is_admin": False,
                "saved_item_ids": ["product-1"]
            }
        ]
        
        response = client.delete("/api/v1/users/test-user-id/saved-items/nonexistent-product")
        
        assert response.status_code == 200
        data = response.json()
        assert data["saved_item_ids"] == ["product-1"]
    
    @patch('app.services.user_service.load_all')
    def test_unsave_item_from_empty_list(self, mock_load_users):
        mock_load_users.return_value = [
            {
                "user_id": "test-user-id",
                "username": "testuser",
                "email": "test@example.com",
                "hashed_password": "$2b$12$hash",
                "is_admin": False,
                "saved_item_ids": []
            }
        ]
        
        response = client.delete("/api/v1/users/test-user-id/saved-items/product-1")
        
        assert response.status_code == 200
        data = response.json()
        assert data["saved_item_ids"] == []

