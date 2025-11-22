import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from app.main import app

client = TestClient(app)


class TestProductCRUD:
    
    @patch('app.services.product_service.load_all')
    @patch('app.services.product_service.save_all')
    @patch('uuid.uuid4')
    def test_create_product_success(self, mock_uuid, mock_save, mock_load):
        mock_load.return_value = []
        mock_uuid.return_value = MagicMock()
        mock_uuid.return_value.__str__ = MagicMock(return_value="test-product-id-123")
        
        product_data = {
            "product_name": "Test Product",
            "category": ["electronics"],
            "discounted_price": 99.99,
            "actual_price": 129.99,
            "discount_percentage": "23%",
            "rating": 4.5,
            "rating_count": 100,
            "about_product": "A great test product",
            "user_id": ["user1"],
            "user_name": ["John"],
            "review_id": ["rev1"],
            "review_title": ["Great!"],
            "review_content": "Excellent product",
            "img_link": "https://example.com/img.jpg",
            "product_link": "https://example.com/product"
        }
        
        response = client.post("/api/v1/products", json=product_data)
        
        assert response.status_code == 201
        data = response.json()
        assert data["product_id"] == "test-product-id-123"
        assert data["product_name"] == "Test Product"
        assert data["discounted_price"] == 99.99
        assert data["rating"] == 4.5
        mock_save.assert_called_once()
    
    @patch('app.services.product_service.load_all')
    @patch('app.services.product_service.save_all')
    @patch('uuid.uuid4')
    def test_create_product_trimmed_fields(self, mock_uuid, mock_save, mock_load):
        mock_load.return_value = []
        mock_uuid.return_value = MagicMock()
        mock_uuid.return_value.__str__ = MagicMock(return_value="test-id")
        
        product_data = {
            "product_name": "  Test Product  ",
            "category": ["electronics"],
            "discounted_price": 99.99,
            "actual_price": 129.99,
            "discount_percentage": "  23%  ",
            "rating": 4.5,
            "rating_count": 100,
            "about_product": "  A great product  ",
            "user_id": [],
            "user_name": [],
            "review_id": [],
            "review_title": [],
            "review_content": "  Review content  ",
            "img_link": "  https://example.com/img.jpg  ",
            "product_link": "  https://example.com/product  "
        }
        
        response = client.post("/api/v1/products", json=product_data)
        
        assert response.status_code == 201
        data = response.json()
        assert data["product_name"] == "Test Product"
        assert data["discount_percentage"] == "23%"
        assert data["about_product"] == "A great product"
    
    @patch('app.services.product_service.load_all')
    def test_create_product_validation_error(self, mock_load):
        mock_load.return_value = []
        
        invalid_product = {
            "product_name": "Test",
            "discounted_price": "not a number"
        }
        
        response = client.post("/api/v1/products", json=invalid_product)
        
        assert response.status_code == 422
    
    @patch('app.services.product_service.load_all')
    @patch('app.services.product_service.save_all')
    def test_update_product_success(self, mock_save, mock_load):
        mock_load.return_value = [
            {
                "product_id": "existing-id",
                "product_name": "Old Name",
                "category": ["old"],
                "discounted_price": 50.0,
                "actual_price": 100.0,
                "discount_percentage": "50%",
                "rating": 3.0,
                "rating_count": 50,
                "about_product": "Old description",
                "user_id": [],
                "user_name": [],
                "review_id": [],
                "review_title": [],
                "review_content": "Old review",
                "img_link": "https://old.com/img.jpg",
                "product_link": "https://old.com/product"
            }
        ]
        
        update_data = {
            "product_name": "New Name",
            "category": ["new"],
            "discounted_price": 75.0,
            "actual_price": 100.0,
            "discount_percentage": "25%",
            "rating": 4.5,
            "rating_count": 100,
            "about_product": "New description",
            "user_id": [],
            "user_name": [],
            "review_id": [],
            "review_title": [],
            "review_content": "New review",
            "img_link": "https://new.com/img.jpg",
            "product_link": "https://new.com/product"
        }
        
        response = client.put("/api/v1/products/existing-id", json=update_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["product_id"] == "existing-id"
        assert data["product_name"] == "New Name"
        assert data["discounted_price"] == 75.0
        assert data["rating"] == 4.5
        mock_save.assert_called_once()
    
    @patch('app.services.product_service.load_all')
    def test_update_product_not_found(self, mock_load):
        mock_load.return_value = []
        
        update_data = {
            "product_name": "New Name",
            "category": [],
            "discounted_price": 99.99,
            "actual_price": 129.99,
            "discount_percentage": "23%",
            "rating": 4.5,
            "rating_count": 100,
            "about_product": "Description",
            "user_id": [],
            "user_name": [],
            "review_id": [],
            "review_title": [],
            "review_content": "Review",
            "img_link": "https://example.com/img.jpg",
            "product_link": "https://example.com/product"
        }
        
        response = client.put("/api/v1/products/nonexistent-id", json=update_data)
        
        assert response.status_code == 404
        assert "could not find" in response.json()["message"].lower()
    
    @patch('app.services.product_service.load_all')
    def test_update_product_validation_error(self, mock_load):
        mock_load.return_value = [
            {
                "product_id": "existing-id",
                "product_name": "Old",
                "category": [],
                "discounted_price": 50.0,
                "actual_price": 100.0,
                "discount_percentage": "50%",
                "rating": 3.0,
                "rating_count": 50,
                "about_product": "Desc",
                "user_id": [],
                "user_name": [],
                "review_id": [],
                "review_title": [],
                "review_content": "Review",
                "img_link": "https://example.com/img.jpg",
                "product_link": "https://example.com/product"
            }
        ]
        
        invalid_update = {
            "product_name": "New",
            "discounted_price": "not a number"
        }
        
        response = client.put("/api/v1/products/existing-id", json=invalid_update)
        
        assert response.status_code == 422
    
    @patch('app.services.product_service.load_all')
    @patch('app.services.product_service.save_all')
    def test_delete_product_success(self, mock_save, mock_load):
        mock_load.return_value = [
            {
                "product_id": "product-to-delete",
                "product_name": "Delete Me",
                "category": [],
                "discounted_price": 50.0,
                "actual_price": 100.0,
                "discount_percentage": "50%",
                "rating": 3.0,
                "rating_count": 50,
                "about_product": "Desc",
                "user_id": [],
                "user_name": [],
                "review_id": [],
                "review_title": [],
                "review_content": "Review",
                "img_link": "https://example.com/img.jpg",
                "product_link": "https://example.com/product"
            },
            {
                "product_id": "keep-me",
                "product_name": "Keep This",
                "category": [],
                "discounted_price": 50.0,
                "actual_price": 100.0,
                "discount_percentage": "50%",
                "rating": 3.0,
                "rating_count": 50,
                "about_product": "Desc",
                "user_id": [],
                "user_name": [],
                "review_id": [],
                "review_title": [],
                "review_content": "Review",
                "img_link": "https://example.com/img.jpg",
                "product_link": "https://example.com/product"
            }
        ]
        
        response = client.delete("/api/v1/products/product-to-delete")
        
        assert response.status_code == 204
        
        saved_data = mock_save.call_args[0][0]
        assert len(saved_data) == 1
        assert saved_data[0]["product_id"] == "keep-me"
        assert all(p["product_id"] != "product-to-delete" for p in saved_data)
    
    @patch('app.services.product_service.load_all')
    def test_delete_product_not_found(self, mock_load):
        mock_load.return_value = []
        
        response = client.delete("/api/v1/products/nonexistent-id")
        
        assert response.status_code == 404
        assert "could not find" in response.json()["message"].lower()
    
    @patch('app.services.product_service.load_all')
    @patch('app.services.product_service.save_all')
    def test_delete_product_from_multiple_products(self, mock_save, mock_load):
        mock_load.return_value = [
            {
                "product_id": "product-1",
                "product_name": "Product 1",
                "category": [],
                "discounted_price": 50.0,
                "actual_price": 100.0,
                "discount_percentage": "50%",
                "rating": 3.0,
                "rating_count": 50,
                "about_product": "Desc",
                "user_id": [],
                "user_name": [],
                "review_id": [],
                "review_title": [],
                "review_content": "Review",
                "img_link": "https://example.com/img.jpg",
                "product_link": "https://example.com/product"
            },
            {
                "product_id": "product-2",
                "product_name": "Product 2",
                "category": [],
                "discounted_price": 50.0,
                "actual_price": 100.0,
                "discount_percentage": "50%",
                "rating": 3.0,
                "rating_count": 50,
                "about_product": "Desc",
                "user_id": [],
                "user_name": [],
                "review_id": [],
                "review_title": [],
                "review_content": "Review",
                "img_link": "https://example.com/img.jpg",
                "product_link": "https://example.com/product"
            },
            {
                "product_id": "product-3",
                "product_name": "Product 3",
                "category": [],
                "discounted_price": 50.0,
                "actual_price": 100.0,
                "discount_percentage": "50%",
                "rating": 3.0,
                "rating_count": 50,
                "about_product": "Desc",
                "user_id": [],
                "user_name": [],
                "review_id": [],
                "review_title": [],
                "review_content": "Review",
                "img_link": "https://example.com/img.jpg",
                "product_link": "https://example.com/product"
            }
        ]
        
        response = client.delete("/api/v1/products/product-2")
        
        assert response.status_code == 204
        
        saved_data = mock_save.call_args[0][0]
        assert len(saved_data) == 2
        product_ids = [p["product_id"] for p in saved_data]
        assert "product-1" in product_ids
        assert "product-3" in product_ids
        assert "product-2" not in product_ids
    
    @patch('app.services.product_service.load_all')
    @patch('app.services.product_service.save_all')
    @patch('uuid.uuid4')
    def test_create_product_with_empty_lists(self, mock_uuid, mock_save, mock_load):
        mock_load.return_value = []
        mock_uuid.return_value = MagicMock()
        mock_uuid.return_value.__str__ = MagicMock(return_value="test-id")
        
        product_data = {
            "product_name": "Test Product",
            "category": [],
            "discounted_price": 99.99,
            "actual_price": 129.99,
            "discount_percentage": "23%",
            "rating": 4.5,
            "rating_count": 100,
            "about_product": "Description",
            "user_id": [],
            "user_name": [],
            "review_id": [],
            "review_title": [],
            "review_content": "Review",
            "img_link": "https://example.com/img.jpg",
            "product_link": "https://example.com/product"
        }
        
        response = client.post("/api/v1/products", json=product_data)
        
        assert response.status_code == 201
        data = response.json()
        assert data["category"] == []
        assert data["user_id"] == []
        assert data["review_id"] == []

