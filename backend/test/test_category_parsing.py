"""
Simple tests for category string parsing in filtering.

Tests the category parsing logic that handles multiple categories
separated by '*' delimiter in the filter_product_list function.
"""

import pytest
from app.services.filtering import filter_product_list


class TestCategoryParsing:
    """Simple tests for category string parsing"""

    # Test products with different categories
    SAMPLE_PRODUCTS = [
        {
            "product_id": "1",
            "product_name": "Laptop",
            "category": ["electronics", "computers"],
            "discounted_price": 800.0
        },
        {
            "product_id": "2", 
            "product_name": "Mouse",
            "category": ["electronics", "accessories"],
            "discounted_price": 25.0
        },
        {
            "product_id": "3",
            "product_name": "Shoes",
            "category": ["footwear", "fashion"],
            "discounted_price": 60.0
        },
        {
            "product_id": "4",
            "product_name": "Phone Case",
            "category": ["accessories", "mobile"],
            "discounted_price": 15.0
        }
    ]

    def test_single_category_filter(self):
        """Test filtering with single category"""
        result = filter_product_list(self.SAMPLE_PRODUCTS, "electronics")
        
        # Should return laptop and mouse (both have electronics category)
        assert len(result) == 2
        product_names = [p["product_name"] for p in result]
        assert "Laptop" in product_names
        assert "Mouse" in product_names

    def test_multiple_categories_with_star_delimiter(self):
        """Test filtering with multiple categories separated by *"""
        result = filter_product_list(self.SAMPLE_PRODUCTS, "electronics*accessories")
        
        # Should return laptop, mouse, and phone case
        # (electronics: laptop, mouse) + (accessories: mouse, phone case)
        assert len(result) == 3
        product_names = [p["product_name"] for p in result]
        assert "Laptop" in product_names
        assert "Mouse" in product_names  
        assert "Phone Case" in product_names

    def test_three_categories_with_star_delimiter(self):
        """Test filtering with three categories"""
        result = filter_product_list(self.SAMPLE_PRODUCTS, "electronics*footwear*mobile")
        
        # Should return laptop, mouse, shoes, phone case
        assert len(result) == 4  # All products match at least one category
        product_names = [p["product_name"] for p in result]
        assert "Laptop" in product_names     # electronics
        assert "Mouse" in product_names      # electronics  
        assert "Shoes" in product_names      # footwear
        assert "Phone Case" in product_names # mobile

    def test_nonexistent_category_returns_empty(self):
        """Test that filtering with non-existent category returns empty list"""
        result = filter_product_list(self.SAMPLE_PRODUCTS, "nonexistent")
        
        assert len(result) == 0

