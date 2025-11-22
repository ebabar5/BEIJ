import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from app.main import app

client = TestClient(app)


class TestSearchEndpoints:
    
    def test_no_search_entry(self):
        response = client.get("/api/v1/previews/search/")
        
        assert response.status_code == 200
        assert response.json() == "Please enter a search query"
    
    @patch('app.routers.previews_router.parse_to_previews')
    @patch('app.routers.previews_router.keyword_search')
    def test_strict_search_single_keyword(self, mock_keyword_search, mock_parse_to_previews):
        mock_products = [
            {
                "product_id": "prod-1",
                "product_name": "Test Product HDMI",
                "category": "Electronics",
                "discounted_price": 29.99,
                "rating": 4.5
            }
        ]
        mock_previews = [
            {
                "product_id": "prod-1",
                "product_name": "Test Product HDMI",
                "discounted_price": 29.99,
                "rating": 4.5
            }
        ]
        mock_keyword_search.return_value = mock_products
        mock_parse_to_previews.return_value = mock_previews
        
        response = client.get("/api/v1/previews/search/HDMI")
        
        assert response.status_code == 200
        mock_keyword_search.assert_called_once_with(["HDMI"])
        mock_parse_to_previews.assert_called_once_with(mock_products)
        assert len(response.json()) == 1
        assert response.json()[0]["product_id"] == "prod-1"
    
    @patch('app.routers.previews_router.parse_to_previews')
    @patch('app.routers.previews_router.keyword_search')
    def test_strict_search_multiple_keywords(self, mock_keyword_search, mock_parse_to_previews):
        mock_products = [
            {
                "product_id": "prod-1",
                "product_name": "Test Product HDMI Cable",
                "category": "Electronics",
                "discounted_price": 29.99,
                "rating": 4.5
            }
        ]
        mock_previews = [
            {
                "product_id": "prod-1",
                "product_name": "Test Product HDMI Cable",
                "discounted_price": 29.99,
                "rating": 4.5
            }
        ]
        mock_keyword_search.return_value = mock_products
        mock_parse_to_previews.return_value = mock_previews
        
        response = client.get("/api/v1/previews/search/HDMI%20Cable")
        
        assert response.status_code == 200
        mock_keyword_search.assert_called_once_with(["HDMI", "Cable"])
        assert len(response.json()) == 1
    
    @patch('app.routers.previews_router.parse_to_previews')
    @patch('app.routers.previews_router.keyword_search')
    def test_strict_search_with_filter(self, mock_keyword_search, mock_parse_to_previews):
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
        mock_keyword_search.return_value = mock_products
        mock_parse_to_previews.return_value = mock_previews
        
        response = client.get("/api/v1/previews/search/HDMI&Cables")
        
        assert response.status_code == 200
        mock_keyword_search.assert_called_once_with(["HDMI"], filter="Cables")
        assert len(response.json()) == 1
    
    @patch('app.routers.previews_router.parse_to_previews')
    @patch('app.routers.previews_router.keyword_search')
    def test_strict_search_multiple_keywords_with_filter(self, mock_keyword_search, mock_parse_to_previews):
        mock_products = []
        mock_previews = []
        mock_keyword_search.return_value = mock_products
        mock_parse_to_previews.return_value = mock_previews
        
        response = client.get("/api/v1/previews/search/HDMI%20Cable&Electronics")
        
        assert response.status_code == 200
        mock_keyword_search.assert_called_once_with(["HDMI", "Cable"], filter="Electronics")
        assert response.json() == []
    
    @patch('app.routers.previews_router.parse_to_previews')
    @patch('app.routers.previews_router.keyword_search')
    def test_strict_search_empty_results(self, mock_keyword_search, mock_parse_to_previews):
        mock_keyword_search.return_value = []
        mock_parse_to_previews.return_value = []
        
        response = client.get("/api/v1/previews/search/nonexistent")
        
        assert response.status_code == 200
        assert response.json() == []
    
    @patch('app.routers.previews_router.parse_to_previews')
    @patch('app.routers.previews_router.keyword_search')
    def test_wide_search_single_keyword(self, mock_keyword_search, mock_parse_to_previews):
        mock_products = [
            {
                "product_id": "prod-1",
                "product_name": "Test Product HDMI",
                "category": "Electronics",
                "discounted_price": 29.99,
                "rating": 4.5
            }
        ]
        mock_previews = [
            {
                "product_id": "prod-1",
                "product_name": "Test Product HDMI",
                "discounted_price": 29.99,
                "rating": 4.5
            }
        ]
        mock_keyword_search.return_value = mock_products
        mock_parse_to_previews.return_value = mock_previews
        
        response = client.get("/api/v1/previews/search/w=HDMI")
        
        assert response.status_code == 200
        mock_keyword_search.assert_called_once_with(["HDMI"])
        mock_parse_to_previews.assert_called_once_with(mock_products)
        assert len(response.json()) == 1
    
    @patch('app.routers.previews_router.parse_to_previews')
    @patch('app.routers.previews_router.keyword_search')
    def test_wide_search_multiple_keywords(self, mock_keyword_search, mock_parse_to_previews):
        mock_products = [
            {
                "product_id": "prod-1",
                "product_name": "Test Product HDMI Cable",
                "category": "Electronics",
                "discounted_price": 29.99,
                "rating": 4.5
            }
        ]
        mock_previews = [
            {
                "product_id": "prod-1",
                "product_name": "Test Product HDMI Cable",
                "discounted_price": 29.99,
                "rating": 4.5
            }
        ]
        mock_keyword_search.return_value = mock_products
        mock_parse_to_previews.return_value = mock_previews
        
        response = client.get("/api/v1/previews/search/w=HDMI%20Cable")
        
        assert response.status_code == 200
        mock_keyword_search.assert_called_once_with(["HDMI", "Cable"])
        assert len(response.json()) == 1
    
    @patch('app.routers.previews_router.parse_to_previews')
    @patch('app.routers.previews_router.keyword_search')
    def test_wide_search_with_filter(self, mock_keyword_search, mock_parse_to_previews):
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
        mock_keyword_search.return_value = mock_products
        mock_parse_to_previews.return_value = mock_previews
        
        response = client.get("/api/v1/previews/search/w=HDMI&Cables")
        
        assert response.status_code == 200
        mock_keyword_search.assert_called_once_with(["HDMI"], filter="Cables")
        assert len(response.json()) == 1
    
    @patch('app.routers.previews_router.parse_to_previews')
    @patch('app.routers.previews_router.keyword_search')
    def test_wide_search_multiple_keywords_with_filter(self, mock_keyword_search, mock_parse_to_previews):
        mock_products = []
        mock_previews = []
        mock_keyword_search.return_value = mock_products
        mock_parse_to_previews.return_value = mock_previews
        
        response = client.get("/api/v1/previews/search/w=HDMI%20Cable&Electronics")
        
        assert response.status_code == 200
        mock_keyword_search.assert_called_once_with(["HDMI", "Cable"], filter="Electronics")
        assert response.json() == []
    
    @patch('app.routers.previews_router.parse_to_previews')
    @patch('app.routers.previews_router.keyword_search')
    def test_wide_search_empty_results(self, mock_keyword_search, mock_parse_to_previews):
        mock_keyword_search.return_value = []
        mock_parse_to_previews.return_value = []
        
        response = client.get("/api/v1/previews/search/w=nonexistent")
        
        assert response.status_code == 200
        assert response.json() == []
    
    @patch('app.routers.previews_router.parse_to_previews')
    @patch('app.routers.previews_router.keyword_search')
    def test_strict_search_special_characters(self, mock_keyword_search, mock_parse_to_previews):
        mock_keyword_search.return_value = []
        mock_parse_to_previews.return_value = []
        
        response = client.get("/api/v1/previews/search/test%20product")
        
        assert response.status_code == 200
        mock_keyword_search.assert_called_once_with(["test", "product"])
    
    @patch('app.routers.previews_router.parse_to_previews')
    @patch('app.routers.previews_router.keyword_search')
    def test_wide_search_special_characters(self, mock_keyword_search, mock_parse_to_previews):
        mock_keyword_search.return_value = []
        mock_parse_to_previews.return_value = []
        
        response = client.get("/api/v1/previews/search/w=test%20product")
        
        assert response.status_code == 200
        mock_keyword_search.assert_called_once_with(["test", "product"])
    
    @patch('app.routers.previews_router.parse_to_previews')
    @patch('app.routers.previews_router.keyword_search')
    def test_strict_search_empty_string(self, mock_keyword_search, mock_parse_to_previews):
        mock_keyword_search.return_value = []
        mock_parse_to_previews.return_value = []
        
        response = client.get("/api/v1/previews/search/")
        
        assert response.status_code == 200
        assert response.json() == "Please enter a search query"
    
    @patch('app.routers.previews_router.parse_to_previews')
    @patch('app.routers.previews_router.keyword_search')
    def test_wide_search_empty_string(self, mock_keyword_search, mock_parse_to_previews):
        mock_keyword_search.return_value = []
        mock_parse_to_previews.return_value = []
        
        response = client.get("/api/v1/previews/search/w=")
        
        assert response.status_code == 200
        mock_keyword_search.assert_called_once_with(["w="])

