"""
Basic tests for main API endpoints.

Simple tests to verify that the core API endpoints are working correctly
and return expected responses. Tests actual HTTP endpoints rather than
just business logic functions.
"""

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


class TestBasicAPIEndpoints:
    """Simple tests for core API endpoints"""

    def test_health_endpoint_returns_ok(self):
        """Test that /health endpoint returns status ok"""
        response = client.get("/health")
        
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}

    def test_get_products_endpoint_works(self):
        """Test that /products endpoint returns a list"""
        response = client.get("/api/v1/products")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    def test_get_single_product_not_found(self):
        """Test that getting non-existent product returns 404"""
        response = client.get("/api/v1/products/nonexistent-id")
        
        assert response.status_code == 404
        assert "message" in response.json()
        assert "could not find" in response.json()["message"].lower()

    def test_home_endpoint_works(self):
        """Test that / (home) endpoint returns status ok"""
        response = client.get("/")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert "message" in data
        assert "docs" in data
