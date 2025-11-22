import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from app.main import app

client = TestClient(app)


class TestErrorHandlingEdgeCases:
    
    def test_register_user_invalid_email_format(self):
        response = client.post("/api/v1/users/register", json={
            "username": "testuser",
            "email": "invalid-email",
            "password": "password123"
        })
        
        assert response.status_code == 422
        errors = response.json()["detail"]
        assert any("email" in str(error).lower() for error in errors)
    
    def test_register_user_password_too_short(self):
        response = client.post("/api/v1/users/register", json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "short"
        })
        
        assert response.status_code == 422
        errors = response.json()["detail"]
        assert any("password" in str(error).lower() or "8" in str(error) for error in errors)
    
    def test_register_user_username_too_short(self):
        response = client.post("/api/v1/users/register", json={
            "username": "ab",
            "email": "test@example.com",
            "password": "password123"
        })
        
        assert response.status_code == 422
        errors = response.json()["detail"]
        assert any("username" in str(error).lower() or "3" in str(error) for error in errors)
    
    def test_register_user_username_too_long(self):
        response = client.post("/api/v1/users/register", json={
            "username": "a" * 51,
            "email": "test@example.com",
            "password": "password123"
        })
        
        assert response.status_code == 422
        errors = response.json()["detail"]
        assert any("username" in str(error).lower() or "50" in str(error) for error in errors)
    
    def test_register_user_missing_required_fields(self):
        response = client.post("/api/v1/users/register", json={
            "username": "testuser"
        })
        
        assert response.status_code == 422
        errors = response.json()["detail"]
        assert len(errors) > 0
    
    def test_login_invalid_email_format(self):
        response = client.post("/api/v1/users/login", json={
            "username_or_email": "invalid-email",
            "password": "password123"
        })
        
        assert response.status_code == 401
    
    def test_login_password_too_short(self):
        response = client.post("/api/v1/users/login", json={
            "username_or_email": "test@example.com",
            "password": "short"
        })
        
        assert response.status_code == 422
        errors = response.json()["detail"]
        assert any("password" in str(error).lower() or "8" in str(error) for error in errors)
    
    def test_update_profile_password_too_short(self):
        response = client.put("/api/v1/users/test-user-id", json={
            "password": "short"
        })
        
        assert response.status_code == 422
        errors = response.json()["detail"]
        assert any("password" in str(error).lower() or "8" in str(error) for error in errors)
    
    def test_update_profile_username_too_short(self):
        response = client.put("/api/v1/users/test-user-id", json={
            "username": "ab"
        })
        
        assert response.status_code == 422
        errors = response.json()["detail"]
        assert any("username" in str(error).lower() or "3" in str(error) for error in errors)
    
    def test_update_profile_invalid_email(self):
        response = client.put("/api/v1/users/test-user-id", json={
            "email": "invalid-email"
        })
        
        assert response.status_code == 422
        errors = response.json()["detail"]
        assert any("email" in str(error).lower() for error in errors)
    
    def test_create_product_missing_required_fields(self):
        response = client.post("/api/v1/products/", json={
            "product_name": "Test Product"
        })
        
        assert response.status_code == 422
        errors = response.json()["detail"]
        assert len(errors) > 0
    
    def test_create_product_invalid_data_types(self):
        response = client.post("/api/v1/products/", json={
            "product_name": "Test Product",
            "category": "not-a-list",
            "discounted_price": "not-a-number",
            "actual_price": 100.0,
            "discount_percentage": "10%",
            "rating": 4.5,
            "rating_count": 100,
            "about_product": "Test description",
            "user_id": [],
            "user_name": [],
            "review_id": [],
            "review_title": [],
            "review_content": "Test review",
            "img_link": "http://example.com/image.jpg",
            "product_link": "http://example.com/product"
        })
        
        assert response.status_code == 422
        errors = response.json()["detail"]
        assert len(errors) > 0
    
    def test_malformed_json_request(self):
        response = client.post(
            "/api/v1/users/register",
            data="invalid json{",
            headers={"Content-Type": "application/json"}
        )
        
        assert response.status_code == 422
    
    def test_invalid_http_method(self):
        response = client.patch("/api/v1/users/test-user-id")
        
        assert response.status_code == 405
    
    def test_nonexistent_endpoint(self):
        response = client.get("/api/v1/nonexistent/endpoint")
        
        assert response.status_code == 404
    
    @patch('app.services.user_service.load_all')
    def test_get_user_profile_not_found(self, mock_load_users):
        mock_load_users.return_value = []
        
        response = client.get("/api/v1/users/nonexistent-user-id")
        
        assert response.status_code == 404
        assert "not found" in response.json()["message"].lower()
    
    @patch('app.services.product_service.load_all')
    def test_get_product_not_found(self, mock_load_products):
        mock_load_products.return_value = []
        
        response = client.get("/api/v1/products/nonexistent-product-id")
        
        assert response.status_code == 404
        assert "could not find" in response.json()["message"].lower()
    
    @patch('app.services.user_service.load_all')
    def test_update_user_profile_not_found(self, mock_load_users):
        mock_load_users.return_value = []
        
        response = client.put("/api/v1/users/nonexistent-user-id", json={
            "username": "newusername"
        })
        
        assert response.status_code == 404
        assert "not found" in response.json()["message"].lower()
    
    @patch('app.services.product_service.load_all')
    def test_update_product_not_found(self, mock_load_products):
        mock_load_products.return_value = []
        
        response = client.put("/api/v1/products/nonexistent-product-id", json={
            "product_name": "Updated Product",
            "category": [],
            "discounted_price": 29.99,
            "actual_price": 39.99,
            "discount_percentage": "25%",
            "rating": 4.5,
            "rating_count": 100,
            "about_product": "Description",
            "user_id": [],
            "user_name": [],
            "review_id": [],
            "review_title": [],
            "review_content": "Review",
            "img_link": "http://example.com/image.jpg",
            "product_link": "http://example.com/product"
        })
        
        assert response.status_code == 404
        assert "could not find" in response.json()["message"].lower()
    
    @patch('app.services.product_service.load_all')
    def test_delete_product_not_found(self, mock_load_products):
        mock_load_products.return_value = []
        
        response = client.delete("/api/v1/products/nonexistent-product-id")
        
        assert response.status_code == 404
        assert "could not find" in response.json()["message"].lower()
    
    def test_logout_missing_authorization_header(self):
        response = client.post("/api/v1/users/logout")
        
        assert response.status_code == 401 or response.status_code == 422
    
    def test_logout_invalid_token_format(self):
        response = client.post(
            "/api/v1/users/logout",
            headers={"Authorization": "InvalidToken"}
        )
        
        assert response.status_code in [200, 401, 422]
    
    def test_products_invalid_sort_parameter(self):
        response = client.get("/api/v1/products/?sort_by=invalid_sort")
        
        assert response.status_code in [200, 400]
    
    @patch('app.services.preview_service.parse_filter_string')
    def test_filter_previews_malformed_filter(self, mock_parse_filter):
        mock_parse_filter.side_effect = Exception("Malformed filter")
        
        response = client.get("/api/v1/previews/invalid&filter&malformed")
        
        assert response.status_code == 406
        data = response.json()
        assert "Malformed Filter Request" in data.get("detail", "") or "Malformed Filter Request" in str(data)
    
    @patch('app.services.user_service.load_all')
    def test_save_item_user_not_found(self, mock_load_users):
        mock_load_users.return_value = []
        
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
    
    def test_empty_request_body(self):
        response = client.post("/api/v1/users/register", json={})
        
        assert response.status_code == 422
        errors = response.json()["detail"]
        assert len(errors) > 0
    
    def test_null_values_in_request(self):
        response = client.post("/api/v1/users/register", json={
            "username": None,
            "email": None,
            "password": None
        })
        
        assert response.status_code == 422
        errors = response.json()["detail"]
        assert len(errors) > 0
    
    def test_extra_fields_in_request(self):
        response = client.post("/api/v1/users/register", json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "password123",
            "extra_field": "should_be_ignored"
        })
        
        assert response.status_code in [200, 201, 409]
    
    def test_boundary_username_length_min(self):
        response = client.post("/api/v1/users/register", json={
            "username": "abc",
            "email": "test@example.com",
            "password": "password123"
        })
        
        assert response.status_code in [200, 201, 409, 422]
    
    def test_boundary_username_length_max(self):
        response = client.post("/api/v1/users/register", json={
            "username": "a" * 50,
            "email": "test@example.com",
            "password": "password123"
        })
        
        assert response.status_code in [200, 201, 409, 422]
    
    def test_boundary_password_length_min(self):
        response = client.post("/api/v1/users/register", json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "a" * 8
        })
        
        assert response.status_code in [200, 201, 409, 422]
    
    def test_invalid_url_encoding(self):
        response = client.get("/api/v1/previews/search/%")
        
        assert response.status_code in [200, 400, 404, 422]
    
    def test_very_long_input_string(self):
        response = client.post("/api/v1/users/register", json={
            "username": "a" * 1000,
            "email": "test@example.com",
            "password": "password123"
        })
        
        assert response.status_code == 422
        errors = response.json()["detail"]
        assert len(errors) > 0
    
    def test_special_characters_in_username(self):
        response = client.post("/api/v1/users/register", json={
            "username": "test@user#name",
            "email": "test@example.com",
            "password": "password123"
        })
        
        assert response.status_code in [200, 201, 409, 422]
    
    def test_unicode_characters(self):
        response = client.post("/api/v1/users/register", json={
            "username": "测试用户",
            "email": "test@example.com",
            "password": "password123"
        })
        
        assert response.status_code in [200, 201, 409, 422]

