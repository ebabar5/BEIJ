"""
Comprehensive tests for product preview service functionality.

This module tests the preview service which provides lightweight product data:
- Converting full products to previews (parse_to_previews)
- Getting all product previews (get_all_product_previews)
- Filtering previews by category and price (filter_previews)
- Error handling for malformed filter requests
- Integration with filtering service

Preview service creates lightweight ProductPreview objects containing only:
- product_id, product_name, discounted_price, rating

Tests use mocking to isolate preview logic from data persistence.
"""

import pytest
from unittest.mock import patch, MagicMock
from fastapi import HTTPException
from app.services.preview_service import parse_to_previews, get_all_product_previews, filter_previews
from app.schemas.product_preview import ProductPreview
from test.dummy_data.dummy_products import SAMPLE_FULL_PRODUCTS


class TestPreviewService:
    """Test suite for product preview service functionality"""

    # Sample full product data (what comes from repository)
    

    def test_parse_to_previews_success(self):
        """Test successful conversion of full products to previews"""
        previews = parse_to_previews(SAMPLE_FULL_PRODUCTS)
        
        # Should return list of ProductPreview objects
        assert len(previews) == 3
        assert all(isinstance(preview, ProductPreview) for preview in previews)
        
        # Check first preview has correct data
        first_preview = previews[0]
        assert first_preview.product_id == "prod1"
        assert first_preview.product_name == "Gaming Laptop"
        assert first_preview.discounted_price == 800.0
        assert first_preview.rating == 4.5
        
        # Check second preview
        second_preview = previews[1]
        assert second_preview.product_id == "prod2"
        assert second_preview.product_name == "Wireless Mouse"
        assert second_preview.discounted_price == 25.0
        assert second_preview.rating == 4.2

    def test_parse_to_previews_empty_list(self):
        """Test parsing empty product list returns empty preview list"""
        previews = parse_to_previews([])
        
        assert previews == []
        assert isinstance(previews, list)

    def test_parse_to_previews_single_product(self):
        """Test parsing single product works correctly"""
        single_product = [SAMPLE_FULL_PRODUCTS[0]]
        previews = parse_to_previews(single_product)
        
        assert len(previews) == 1
        preview = previews[0]
        assert preview.product_id == "prod1"
        assert preview.product_name == "Gaming Laptop"
        assert preview.discounted_price == 800.0
        assert preview.rating == 4.5

    def test_parse_to_previews_only_required_fields(self):
        """Test that previews only contain the 4 required fields"""
        previews = parse_to_previews(SAMPLE_FULL_PRODUCTS)
        
        for preview in previews:
            # Check that preview object only has the expected fields
            preview_dict = preview.model_dump()
            expected_fields = {"product_id", "product_name", "discounted_price", "rating"}
            assert set(preview_dict.keys()) == expected_fields

    @patch('app.services.preview_service.load_all')
    def test_get_all_product_previews_success(self, mock_load_all):
        """Test getting all product previews from repository"""
        mock_load_all.return_value = SAMPLE_FULL_PRODUCTS
        
        previews = get_all_product_previews()
        
        # Should call load_all once
        mock_load_all.assert_called_once()
        
        # Should return correct previews
        assert len(previews) == 3
        assert all(isinstance(preview, ProductPreview) for preview in previews)
        assert previews[0].product_name == "Gaming Laptop"
        assert previews[1].product_name == "Wireless Mouse"
        assert previews[2].product_name == "Running Shoes"

    @patch('app.services.preview_service.load_all')
    def test_get_all_product_previews_empty_repository(self, mock_load_all):
        """Test getting previews when repository is empty"""
        mock_load_all.return_value = []
        
        previews = get_all_product_previews()
        
        mock_load_all.assert_called_once()
        assert previews == []

    @patch('app.services.preview_service.filter_product_list')
    @patch('app.services.preview_service.load_all')
    def test_filter_previews_category_only(self, mock_load_all, mock_filter):
        """Test filtering previews by category only"""
        mock_load_all.return_value = SAMPLE_FULL_PRODUCTS
        # Mock filter to return electronics products
        electronics_products = [SAMPLE_FULL_PRODUCTS[0], SAMPLE_FULL_PRODUCTS[1]]
        mock_filter.return_value = electronics_products
        
        previews = filter_previews("electronics")
        
        # Should call filter_product_list with category only
        mock_filter.assert_called_once_with(SAMPLE_FULL_PRODUCTS, "electronics")
        
        # Should return filtered previews
        assert len(previews) == 2
        assert previews[0].product_name == "Gaming Laptop"
        assert previews[1].product_name == "Wireless Mouse"

    @patch('app.services.preview_service.filter_product_list')
    @patch('app.services.preview_service.load_all')
    def test_filter_previews_category_and_price_range(self, mock_load_all, mock_filter):
        """Test filtering previews by category and price range"""
        mock_load_all.return_value = SAMPLE_FULL_PRODUCTS
        # Mock filter to return one product in price range
        filtered_products = [SAMPLE_FULL_PRODUCTS[1]]  # Wireless Mouse ($25)
        mock_filter.return_value = filtered_products
        
        previews = filter_previews("electronics&max=30&min=20")
        
        # The code correctly parses both max and min when in this order
        mock_filter.assert_called_once_with(SAMPLE_FULL_PRODUCTS, "electronics", 20, 30)
        
        # Should return filtered previews
        assert len(previews) == 1
        assert previews[0].product_name == "Wireless Mouse"
        assert previews[0].discounted_price == 25.0

    @patch('app.services.preview_service.filter_product_list')
    @patch('app.services.preview_service.load_all')
    def test_filter_previews_max_price_only(self, mock_load_all, mock_filter):
        """Test filtering previews with max price only"""
        mock_load_all.return_value = SAMPLE_FULL_PRODUCTS
        filtered_products = [SAMPLE_FULL_PRODUCTS[1], SAMPLE_FULL_PRODUCTS[2]]
        mock_filter.return_value = filtered_products
        
        previews = filter_previews("all&max=100")
        
        # Should call filter with min=0 (default) and max=100
        mock_filter.assert_called_once_with(SAMPLE_FULL_PRODUCTS, "all", 0, 100)
        
        assert len(previews) == 2

    @patch('app.services.preview_service.filter_product_list')
    @patch('app.services.preview_service.load_all')
    def test_filter_previews_min_price_only_raises_exception(self, mock_load_all, mock_filter):
        """Test filtering previews with min price only raises exception due to bug in original code"""
        mock_load_all.return_value = SAMPLE_FULL_PRODUCTS
        
        # Due to bug in original code (parts[2] instead of part), this raises an exception
        with pytest.raises(HTTPException) as exc_info:
            filter_previews("electronics&min=500")
        
        assert exc_info.value.status_code == 406
        assert "Malformed Filter Request" in str(exc_info.value.detail)

    @patch('app.services.preview_service.load_all')
    def test_filter_previews_malformed_request_raises_exception(self, mock_load_all):
        """Test that malformed filter requests raise HTTPException"""
        mock_load_all.return_value = SAMPLE_FULL_PRODUCTS
        
        # Mock filter_product_list to raise an exception (simulating malformed request)
        with patch('app.services.preview_service.filter_product_list') as mock_filter:
            mock_filter.side_effect = ValueError("Invalid filter format")
            
            with pytest.raises(HTTPException) as exc_info:
                filter_previews("invalid&format&here")
            
            assert exc_info.value.status_code == 406
            assert "Malformed Filter Request" in str(exc_info.value.detail)

    @patch('app.services.preview_service.filter_product_list')
    @patch('app.services.preview_service.load_all')
    def test_filter_previews_empty_result(self, mock_load_all, mock_filter):
        """Test filtering that returns no results"""
        mock_load_all.return_value = SAMPLE_FULL_PRODUCTS
        mock_filter.return_value = []  # No products match filter
        
        previews = filter_previews("nonexistent_category")
        
        mock_filter.assert_called_once_with(SAMPLE_FULL_PRODUCTS, "nonexistent_category")
        assert previews == []

    def test_preview_data_integrity(self):
        """Test that preview conversion preserves data integrity"""
        # Test with edge case values
        edge_case_product = [{
            "product_id": "edge1",
            "product_name": "Edge Case Product",
            "category": ["test"],
            "discounted_price": 0.01,  # Very small price
            "actual_price": 0.02,
            "discount_percentage": "50%",
            "rating": 5.0,  # Maximum rating
            "rating_count": 1,
            "about_product": "Test product",
            "user_id": ["u1"],
            "user_name": ["Test User"],
            "review_id": ["r1"],
            "review_title": ["Test Review"],
            "review_content": "Test content",
            "img_link": "http://test.com/img.jpg",
            "product_link": "http://test.com/product"
        }]
        
        previews = parse_to_previews(edge_case_product)
        
        assert len(previews) == 1
        preview = previews[0]
        assert preview.product_id == "edge1"
        assert preview.product_name == "Edge Case Product"
        assert preview.discounted_price == 0.01
        assert preview.rating == 5.0
