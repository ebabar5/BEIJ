"""
Basic test for product filtering functionality.

Simple test to verify that the filtering service correctly filters products
by category and price range. This is a focused test for the core filtering logic.
"""

import pytest
from app.services.filtering import filter_product_list


class TestBasicFiltering:
    """Simple test for product filtering"""

    # Simple test data
    SAMPLE_PRODUCTS = [
        {
            "product_id": "1",
            "product_name": "Laptop",
            "category": ["electronics"],
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
            "category": ["footwear"],
            "discounted_price": 60.0
        }
    ]

    def test_filter_by_category_electronics(self):
        """Test filtering products by electronics category"""
        result = filter_product_list(self.SAMPLE_PRODUCTS, "electronics")
        
        # Should return laptop and mouse (both have electronics category)
        assert len(result) == 2
        product_names = [p["product_name"] for p in result]
        assert "Laptop" in product_names
        assert "Mouse" in product_names
        assert "Shoes" not in product_names

    def test_filter_by_price_range(self):
        """Test filtering products by price range"""
        result = filter_product_list(self.SAMPLE_PRODUCTS, "all", min_price=50, max_price=100)
        
        # Should return only shoes (price 60.0 is between 50-100)
        assert len(result) == 1
        assert result[0]["product_name"] == "Shoes"
        assert result[0]["discounted_price"] == 60.0

    def test_filter_all_category_returns_all_products(self):
        """Test that 'all' category returns all products"""
        result = filter_product_list(self.SAMPLE_PRODUCTS, "all")
        
        # Should return all 3 products
        assert len(result) == 3
        product_names = [p["product_name"] for p in result]
        assert "Laptop" in product_names
        assert "Mouse" in product_names  
        assert "Shoes" in product_names
