"""
Simple test for price validation logic in filtering.

Tests the price normalization and swapping logic that ensures
min_price and max_price are always in the correct order and non-negative.
"""

from app.services.filtering import filter_product_list
from test.dummy_data.simplified_dummy_products import SAMPLE_PRODUCT


class TestPriceValidation:
    """Simple tests for price validation logic"""


    def test_negative_prices_become_zero(self):
        """Test that negative min/max prices are converted to 0"""
        # Both negative should become 0, and when min=0 & max=0, no price filter is applied
        result = filter_product_list(SAMPLE_PRODUCT, "all", min_price=-10, max_price=-5)
        assert len(result) == 1  # All products returned (no price filter when both are 0)

    def test_backwards_prices_get_swapped(self):
        """Test that min > max gets swapped automatically"""
        # min_price=100, max_price=30 should swap to min=30, max=100
        result = filter_product_list(SAMPLE_PRODUCT, "all", min_price=100, max_price=30)
        
        # Product price 50 should be included (30 <= 50 <= 100)
        assert len(result) == 1
        assert result[0]["product_name"] == "Test Product"

    def test_normal_price_range_works(self):
        """Test that normal min < max price range works correctly"""
        # Normal range: min=40, max=60 should include product with price 50
        result = filter_product_list(SAMPLE_PRODUCT, "all", min_price=40, max_price=60)
        assert len(result) == 1
        assert result[0]["discounted_price"] == 50.0
