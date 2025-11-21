"""
Comprehensive tests for product sorting and filtering functionality.

This module tests all sorting options in the product_service.list_products function:
- Name sorting (default and explicit)
- Price sorting (ascending and descending)
- Rating sorting (descending with rating_count tiebreaker)
- Invalid sort parameter handling
- Edge cases (empty data, identical values, missing fields)

Tests use mocking to isolate the sorting logic from data persistence.
"""

import pytest
from unittest.mock import patch
from fastapi import HTTPException
from app.services.product_service import list_products


class TestProductSorting:
    """Test suite for product sorting functionality"""

    # Sample data with varied values for comprehensive testing
    SAMPLE_PRODUCTS = [
        {
            "product_id": "prod1",
            "product_name": "Zebra Shoes",
            "category": ["footwear"],
            "discounted_price": 50.0,
            "actual_price": 100.0,
            "discount_percentage": "50%",
            "rating": 4.5,
            "rating_count": 100,
            "about_product": "Great shoes",
            "user_id": ["u1"],
            "user_name": ["User One"],
            "review_id": ["r1"],
            "review_title": ["Excellent Quality"],
            "review_content": "Excellent",
            "img_link": "http://example.com/zebra.jpg",
            "product_link": "http://example.com/zebra"
        },
        {
            "product_id": "prod2", 
            "product_name": "Alpha Boots",
            "category": ["footwear"],
            "discounted_price": 75.0,
            "actual_price": 150.0,
            "discount_percentage": "50%",
            "rating": 4.8,
            "rating_count": 50,
            "about_product": "Premium boots",
            "user_id": ["u2"],
            "user_name": ["User Two"],
            "review_id": ["r2"],
            "review_title": ["Amazing Product"],
            "review_content": "Amazing",
            "img_link": "http://example.com/alpha.jpg",
            "product_link": "http://example.com/alpha"
        },
        {
            "product_id": "prod3",
            "product_name": "Beta Sneakers",
            "category": ["footwear"],
            "discounted_price": 25.0,
            "actual_price": 50.0,
            "discount_percentage": "50%",
            "rating": 3.9,
            "rating_count": 200,
            "about_product": "Comfortable sneakers",
            "user_id": ["u3"],
            "user_name": ["User Three"],
            "review_id": ["r3"],
            "review_title": ["Good Value"],
            "review_content": "Good value",
            "img_link": "http://example.com/beta.jpg",
            "product_link": "http://example.com/beta"
        }
    ]

    # Products with identical ratings for tiebreaker testing
    IDENTICAL_RATING_PRODUCTS = [
        {
            "product_id": "tie1",
            "product_name": "Product A",
            "category": ["test"],
            "discounted_price": 10.0,
            "actual_price": 20.0,
            "discount_percentage": "50%",
            "rating": 4.0,
            "rating_count": 100,  # Higher count should come first
            "about_product": "Test product",
            "user_id": ["u1"],
            "user_name": ["User"],
            "review_id": ["r1"],
            "review_title": ["Test Review"],
            "review_content": "Test",
            "img_link": "http://example.com/a.jpg",
            "product_link": "http://example.com/a"
        },
        {
            "product_id": "tie2",
            "product_name": "Product B",
            "category": ["test"],
            "discounted_price": 15.0,
            "actual_price": 30.0,
            "discount_percentage": "50%",
            "rating": 4.0,
            "rating_count": 50,   # Lower count should come second
            "about_product": "Test product",
            "user_id": ["u2"],
            "user_name": ["User"],
            "review_id": ["r2"],
            "review_title": ["Test Review"],
            "review_content": "Test",
            "img_link": "http://example.com/b.jpg",
            "product_link": "http://example.com/b"
        }
    ]

    @patch('app.services.product_service.load_all')
    def test_sort_by_name_default(self, mock_load):
        """Test default sorting (no sort_by parameter) sorts by name alphabetically"""
        mock_load.return_value = self.SAMPLE_PRODUCTS
        
        products = list_products()  # No sort_by parameter
        names = [p.product_name for p in products]
        
        # Should be sorted alphabetically (case-insensitive)
        expected_names = ["Alpha Boots", "Beta Sneakers", "Zebra Shoes"]
        assert names == expected_names

    @patch('app.services.product_service.load_all')
    def test_sort_by_name_explicit(self, mock_load):
        """Test explicit name sorting works the same as default"""
        mock_load.return_value = self.SAMPLE_PRODUCTS
        
        products = list_products(sort_by="name")
        names = [p.product_name for p in products]
        
        expected_names = ["Alpha Boots", "Beta Sneakers", "Zebra Shoes"]
        assert names == expected_names

    @patch('app.services.product_service.load_all')
    def test_sort_by_name_case_insensitive(self, mock_load):
        """Test name sorting is case-insensitive"""
        case_test_products = [
            {**self.SAMPLE_PRODUCTS[0], "product_name": "zebra shoes"},  # lowercase
            {**self.SAMPLE_PRODUCTS[1], "product_name": "ALPHA BOOTS"},  # uppercase
            {**self.SAMPLE_PRODUCTS[2], "product_name": "Beta Sneakers"} # mixed case
        ]
        mock_load.return_value = case_test_products
        
        products = list_products(sort_by="name")
        names = [p.product_name for p in products]
        
        # Should still sort alphabetically regardless of case
        expected_names = ["ALPHA BOOTS", "Beta Sneakers", "zebra shoes"]
        assert names == expected_names

    @patch('app.services.product_service.load_all')
    def test_sort_by_price_ascending(self, mock_load):
        """Test price sorting in ascending order (cheapest first)"""
        mock_load.return_value = self.SAMPLE_PRODUCTS
        
        products = list_products(sort_by="price_asc")
        prices = [p.discounted_price for p in products]
        
        # Should be sorted from lowest to highest price
        expected_prices = [25.0, 50.0, 75.0]
        assert prices == expected_prices
        
        # Verify the products are in correct order
        names = [p.product_name for p in products]
        expected_names = ["Beta Sneakers", "Zebra Shoes", "Alpha Boots"]
        assert names == expected_names

    @patch('app.services.product_service.load_all')
    def test_sort_by_price_descending(self, mock_load):
        """Test price sorting in descending order (most expensive first)"""
        mock_load.return_value = self.SAMPLE_PRODUCTS
        
        products = list_products(sort_by="price_desc")
        prices = [p.discounted_price for p in products]
        
        # Should be sorted from highest to lowest price
        expected_prices = [75.0, 50.0, 25.0]
        assert prices == expected_prices
        
        # Verify the products are in correct order
        names = [p.product_name for p in products]
        expected_names = ["Alpha Boots", "Zebra Shoes", "Beta Sneakers"]
        assert names == expected_names

    @patch('app.services.product_service.load_all')
    def test_sort_by_rating_descending(self, mock_load):
        """Test rating sorting in descending order (highest rated first)"""
        mock_load.return_value = self.SAMPLE_PRODUCTS
        
        products = list_products(sort_by="rating_desc")
        ratings = [p.rating for p in products]
        
        # Should be sorted from highest to lowest rating
        expected_ratings = [4.8, 4.5, 3.9]
        assert ratings == expected_ratings
        
        # Verify the products are in correct order
        names = [p.product_name for p in products]
        expected_names = ["Alpha Boots", "Zebra Shoes", "Beta Sneakers"]
        assert names == expected_names

    @patch('app.services.product_service.load_all')
    def test_sort_by_rating_with_tiebreaker(self, mock_load):
        """Test rating sorting uses rating_count as tiebreaker when ratings are equal"""
        mock_load.return_value = self.IDENTICAL_RATING_PRODUCTS
        
        products = list_products(sort_by="rating_desc")
        
        # Both have rating 4.0, but first should have higher rating_count (100 vs 50)
        assert products[0].rating_count == 100
        assert products[1].rating_count == 50
        assert products[0].product_name == "Product A"
        assert products[1].product_name == "Product B"

    @patch('app.services.product_service.load_all')
    def test_sort_invalid_parameter_raises_http_exception(self, mock_load):
        """Test that invalid sort_by parameter raises HTTPException with 400 status"""
        mock_load.return_value = self.SAMPLE_PRODUCTS
        
        with pytest.raises(HTTPException) as exc_info:
            list_products(sort_by="invalid_sort_option")
        
        assert exc_info.value.status_code == 400
        assert "invalid_sort_option" in str(exc_info.value.detail)
        assert "Support values: name, price_asc, price_desc, rating_desc" in str(exc_info.value.detail)

    @patch('app.services.product_service.load_all')
    def test_sort_empty_product_list(self, mock_load):
        """Test sorting works correctly with empty product list"""
        mock_load.return_value = []
        
        # Test all sort options with empty list
        for sort_by in [None, "name", "price_asc", "price_desc", "rating_desc"]:
            products = list_products(sort_by=sort_by)
            assert products == []

    @patch('app.services.product_service.load_all')
    def test_sort_single_product(self, mock_load):
        """Test sorting works correctly with single product"""
        mock_load.return_value = [self.SAMPLE_PRODUCTS[0]]
        
        # Test all sort options with single product
        for sort_by in [None, "name", "price_asc", "price_desc", "rating_desc"]:
            products = list_products(sort_by=sort_by)
            assert len(products) == 1
            assert products[0].product_name == "Zebra Shoes"

    @patch('app.services.product_service.load_all')
    def test_sort_with_placeholder_handling(self, mock_load):
        """Test sorting works correctly when products have missing/empty fields"""
        products_with_missing_fields = [
            {
                "product_id": "missing1",
                "product_name": "",  # Empty name should become "N/A"
                "category": ["test"],
                "discounted_price": 10.0,
                "actual_price": 20.0,
                "discount_percentage": "",  # Empty discount should become "N/A"
                "rating": 4.0,
                "rating_count": "",  # Empty rating_count should become 0
                "about_product": None,  # None should become "N/A"
                "user_id": ["u1"],
                "user_name": ["User"],
                "review_id": ["r1"],
                "review_title": ["Test"],
                "review_content": "   ",  # Whitespace should become "N/A"
                "img_link": "http://example.com/img.jpg",
                "product_link": "http://example.com/link"
            }
        ]
        mock_load.return_value = products_with_missing_fields
        
        products = list_products(sort_by="name")
        
        # Verify placeholders are applied correctly
        product = products[0]
        assert product.product_name == "N/A"
        assert product.discount_percentage == "N/A"
        assert product.rating_count == 0
        assert product.about_product == "N/A"
        assert product.review_content == "N/A"
