import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from app.main import app

client = TestClient(app)


class TestFilteringEndpoints:
    
    @patch('app.services.preview_service.load_all')
    @patch('app.services.preview_service.parse_to_previews')
    @patch('app.services.preview_service.filter_product_list')
    @patch('app.services.preview_service.parse_filter_string')
    def test_filter_by_category(self, mock_parse_filter, mock_filter_list, mock_parse_to_previews, mock_load_all):
        mock_products = [
            {
                "product_id": "prod-1",
                "product_name": "Test Product",
                "category": "Electronics",
                "discounted_price": 29.99,
                "rating": 4.5
            }
        ]
        mock_previews = [
            {
                "product_id": "prod-1",
                "product_name": "Test Product",
                "discounted_price": 29.99,
                "rating": 4.5
            }
        ]
        mock_load_all.return_value = mock_products
        mock_parse_filter.return_value = {"cat_string": "Electronics"}
        mock_filter_list.return_value = mock_products
        mock_parse_to_previews.return_value = mock_previews
        
        response = client.get("/api/v1/previews/Electronics")
        
        assert response.status_code == 200
        mock_parse_filter.assert_called_once_with("Electronics")
        mock_filter_list.assert_called_once_with(mock_products, cat_string="Electronics")
        assert len(response.json()) == 1
        assert response.json()[0]["product_id"] == "prod-1"
    
    @patch('app.services.preview_service.load_all')
    @patch('app.services.preview_service.parse_to_previews')
    @patch('app.services.preview_service.filter_product_list')
    @patch('app.services.preview_service.parse_filter_string')
    def test_filter_by_multiple_categories(self, mock_parse_filter, mock_filter_list, mock_parse_to_previews, mock_load_all):
        mock_products = [
            {
                "product_id": "prod-1",
                "product_name": "Test Product",
                "category": "Electronics",
                "discounted_price": 29.99,
                "rating": 4.5
            }
        ]
        mock_previews = [
            {
                "product_id": "prod-1",
                "product_name": "Test Product",
                "discounted_price": 29.99,
                "rating": 4.5
            }
        ]
        mock_load_all.return_value = mock_products
        mock_parse_filter.return_value = {"cat_string": "Electronics*Computers"}
        mock_filter_list.return_value = mock_products
        mock_parse_to_previews.return_value = mock_previews
        
        response = client.get("/api/v1/previews/Electronics*Computers")
        
        assert response.status_code == 200
        mock_parse_filter.assert_called_once_with("Electronics*Computers")
        mock_filter_list.assert_called_once_with(mock_products, cat_string="Electronics*Computers")
        assert len(response.json()) == 1
    
    @patch('app.services.preview_service.load_all')
    @patch('app.services.preview_service.parse_to_previews')
    @patch('app.services.preview_service.filter_product_list')
    @patch('app.services.preview_service.parse_filter_string')
    def test_filter_by_category_and_max_price(self, mock_parse_filter, mock_filter_list, mock_parse_to_previews, mock_load_all):
        mock_products = [
            {
                "product_id": "prod-1",
                "product_name": "Test Product",
                "category": "Electronics",
                "discounted_price": 29.99,
                "rating": 4.5
            }
        ]
        mock_previews = [
            {
                "product_id": "prod-1",
                "product_name": "Test Product",
                "discounted_price": 29.99,
                "rating": 4.5
            }
        ]
        mock_load_all.return_value = mock_products
        mock_parse_filter.return_value = {"cat_string": "Electronics", "max_price": 50}
        mock_filter_list.return_value = mock_products
        mock_parse_to_previews.return_value = mock_previews
        
        response = client.get("/api/v1/previews/Electronics&max=50")
        
        assert response.status_code == 200
        mock_parse_filter.assert_called_once_with("Electronics&max=50")
        mock_filter_list.assert_called_once_with(mock_products, cat_string="Electronics", max_price=50)
        assert len(response.json()) == 1
    
    @patch('app.services.preview_service.load_all')
    @patch('app.services.preview_service.parse_to_previews')
    @patch('app.services.preview_service.filter_product_list')
    @patch('app.services.preview_service.parse_filter_string')
    def test_filter_by_category_and_min_price(self, mock_parse_filter, mock_filter_list, mock_parse_to_previews, mock_load_all):
        mock_products = [
            {
                "product_id": "prod-1",
                "product_name": "Test Product",
                "category": "Electronics",
                "discounted_price": 29.99,
                "rating": 4.5
            }
        ]
        mock_previews = [
            {
                "product_id": "prod-1",
                "product_name": "Test Product",
                "discounted_price": 29.99,
                "rating": 4.5
            }
        ]
        mock_load_all.return_value = mock_products
        mock_parse_filter.return_value = {"cat_string": "Electronics", "min_price": 20}
        mock_filter_list.return_value = mock_products
        mock_parse_to_previews.return_value = mock_previews
        
        response = client.get("/api/v1/previews/Electronics&min=20")
        
        assert response.status_code == 200
        mock_parse_filter.assert_called_once_with("Electronics&min=20")
        mock_filter_list.assert_called_once_with(mock_products, cat_string="Electronics", min_price=20)
        assert len(response.json()) == 1
    
    @patch('app.services.preview_service.load_all')
    @patch('app.services.preview_service.parse_to_previews')
    @patch('app.services.preview_service.filter_product_list')
    @patch('app.services.preview_service.parse_filter_string')
    def test_filter_by_category_and_price_range(self, mock_parse_filter, mock_filter_list, mock_parse_to_previews, mock_load_all):
        mock_products = [
            {
                "product_id": "prod-1",
                "product_name": "Test Product",
                "category": "Electronics",
                "discounted_price": 29.99,
                "rating": 4.5
            }
        ]
        mock_previews = [
            {
                "product_id": "prod-1",
                "product_name": "Test Product",
                "discounted_price": 29.99,
                "rating": 4.5
            }
        ]
        mock_load_all.return_value = mock_products
        mock_parse_filter.return_value = {"cat_string": "Electronics", "min_price": 20, "max_price": 50}
        mock_filter_list.return_value = mock_products
        mock_parse_to_previews.return_value = mock_previews
        
        response = client.get("/api/v1/previews/Electronics&min=20&max=50")
        
        assert response.status_code == 200
        mock_parse_filter.assert_called_once_with("Electronics&min=20&max=50")
        mock_filter_list.assert_called_once_with(mock_products, cat_string="Electronics", min_price=20, max_price=50)
        assert len(response.json()) == 1
    
    @patch('app.services.preview_service.load_all')
    @patch('app.services.preview_service.parse_to_previews')
    @patch('app.services.preview_service.filter_product_list')
    @patch('app.services.preview_service.parse_filter_string')
    def test_filter_all_category(self, mock_parse_filter, mock_filter_list, mock_parse_to_previews, mock_load_all):
        mock_products = [
            {
                "product_id": "prod-1",
                "product_name": "Test Product",
                "category": "Electronics",
                "discounted_price": 29.99,
                "rating": 4.5
            }
        ]
        mock_previews = [
            {
                "product_id": "prod-1",
                "product_name": "Test Product",
                "discounted_price": 29.99,
                "rating": 4.5
            }
        ]
        mock_load_all.return_value = mock_products
        mock_parse_filter.return_value = {"cat_string": "all"}
        mock_filter_list.return_value = mock_products
        mock_parse_to_previews.return_value = mock_previews
        
        response = client.get("/api/v1/previews/all")
        
        assert response.status_code == 200
        mock_parse_filter.assert_called_once_with("all")
        mock_filter_list.assert_called_once_with(mock_products, cat_string="all")
        assert len(response.json()) == 1
    
    @patch('app.services.preview_service.load_all')
    @patch('app.services.preview_service.parse_to_previews')
    @patch('app.services.preview_service.filter_product_list')
    @patch('app.services.preview_service.parse_filter_string')
    def test_filter_empty_string(self, mock_parse_filter, mock_filter_list, mock_parse_to_previews, mock_load_all):
        mock_products = [
            {
                "product_id": "prod-1",
                "product_name": "Test Product",
                "category": "Electronics",
                "discounted_price": 29.99,
                "rating": 4.5
            }
        ]
        mock_previews = [
            {
                "product_id": "prod-1",
                "product_name": "Test Product",
                "discounted_price": 29.99,
                "rating": 4.5
            }
        ]
        mock_load_all.return_value = mock_products
        mock_parse_filter.return_value = {"cat_string": "empty"}
        mock_filter_list.return_value = mock_products
        mock_parse_to_previews.return_value = mock_previews
        
        response = client.get("/api/v1/previews/empty")
        
        assert response.status_code == 200
        mock_parse_filter.assert_called_once_with("empty")
        mock_filter_list.assert_called_once_with(mock_products, cat_string="empty")
        assert len(response.json()) == 1
        assert len(response.json()) == 1
    
    @patch('app.services.preview_service.load_all')
    @patch('app.services.preview_service.parse_to_previews')
    @patch('app.services.preview_service.filter_product_list')
    @patch('app.services.preview_service.parse_filter_string')
    def test_filter_empty_results(self, mock_parse_filter, mock_filter_list, mock_parse_to_previews, mock_load_all):
        mock_load_all.return_value = []
        mock_parse_filter.return_value = {"cat_string": "NonexistentCategory"}
        mock_filter_list.return_value = []
        mock_parse_to_previews.return_value = []
        
        response = client.get("/api/v1/previews/NonexistentCategory")
        
        assert response.status_code == 200
        assert response.json() == []
    
    @patch('app.services.preview_service.load_all')
    @patch('app.services.preview_service.parse_filter_string')
    def test_filter_malformed_request(self, mock_parse_filter, mock_load_all):
        mock_load_all.return_value = []
        mock_parse_filter.side_effect = Exception("Malformed filter")
        
        response = client.get("/api/v1/previews/invalid&filter&string")
        
        assert response.status_code == 406
        data = response.json()
        assert "Malformed Filter Request" in data.get("detail", "") or "Malformed Filter Request" in str(data)
    
    @patch('app.services.preview_service.load_all')
    @patch('app.services.preview_service.parse_to_previews')
    @patch('app.services.preview_service.filter_product_list')
    @patch('app.services.preview_service.parse_filter_string')
    def test_filter_by_price_only(self, mock_parse_filter, mock_filter_list, mock_parse_to_previews, mock_load_all):
        mock_products = [
            {
                "product_id": "prod-1",
                "product_name": "Test Product",
                "category": "Electronics",
                "discounted_price": 29.99,
                "rating": 4.5
            }
        ]
        mock_previews = [
            {
                "product_id": "prod-1",
                "product_name": "Test Product",
                "discounted_price": 29.99,
                "rating": 4.5
            }
        ]
        mock_load_all.return_value = mock_products
        mock_parse_filter.return_value = {"cat_string": "all", "max_price": 50}
        mock_filter_list.return_value = mock_products
        mock_parse_to_previews.return_value = mock_previews
        
        response = client.get("/api/v1/previews/all&max=50")
        
        assert response.status_code == 200
        mock_parse_filter.assert_called_once_with("all&max=50")
        mock_filter_list.assert_called_once_with(mock_products, cat_string="all", max_price=50)
        assert len(response.json()) == 1
    
    @patch('app.services.preview_service.load_all')
    @patch('app.services.preview_service.parse_to_previews')
    @patch('app.services.preview_service.filter_product_list')
    @patch('app.services.preview_service.parse_filter_string')
    def test_filter_special_characters_in_category(self, mock_parse_filter, mock_filter_list, mock_parse_to_previews, mock_load_all):
        mock_products = []
        mock_previews = []
        mock_load_all.return_value = mock_products
        mock_parse_filter.return_value = {"cat_string": "Test*Category"}
        mock_filter_list.return_value = mock_products
        mock_parse_to_previews.return_value = mock_previews
        
        response = client.get("/api/v1/previews/Test*Category")
        
        assert response.status_code == 200
        mock_parse_filter.assert_called_once_with("Test*Category")
        assert response.json() == []

