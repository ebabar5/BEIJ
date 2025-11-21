"""
Simple test for rating count normalization helper function.

Tests the _normalize_rating_count utility function that converts
various input formats to clean integer values for rating counts.
"""

import pytest
from app.services.product_service import _normalize_rating_count


class TestRatingCountHelper:
    """Simple tests for rating count normalization"""

    def test_normalize_valid_integer(self):
        """Test normalizing valid integer input"""
        assert _normalize_rating_count(150) == 150
        assert _normalize_rating_count(0) == 0
        assert _normalize_rating_count(999999) == 999999

    def test_normalize_string_with_commas(self):
        """Test normalizing string numbers with commas"""
        assert _normalize_rating_count("1,500") == 1500
        assert _normalize_rating_count("24,269") == 24269
        assert _normalize_rating_count("1,000,000") == 1000000

    def test_normalize_none_and_empty_values(self):
        """Test that None and empty values return 0"""
        assert _normalize_rating_count(None) == 0
        assert _normalize_rating_count("") == 0
        assert _normalize_rating_count("   ") == 0  # whitespace only

    def test_normalize_invalid_values(self):
        """Test that invalid values return 0"""
        assert _normalize_rating_count("not_a_number") == 0
        assert _normalize_rating_count("abc123") == 0
        assert _normalize_rating_count("12.5.6") == 0  # invalid format
