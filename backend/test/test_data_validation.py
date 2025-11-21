"""
Focused tests for Pydantic schema validation.

This module tests the core data validation functionality of Pydantic schemas:
- ProductCreate validation (required fields, data types)
- UserCreate validation (email format, field constraints)
- Product schema validation (complex data structures)
- Invalid data rejection (wrong types, missing fields)
- Edge cases (boundary values, empty data)

These tests ensure data integrity and proper error handling at the schema level.
"""

import pytest
from pydantic import ValidationError
from app.schemas.product import Product, ProductCreate, ProductUpdate
from app.schemas.user import User, UserCreate, UserResponse, UserLogin
from app.schemas.product_preview import ProductPreview


class TestDataValidation:
    """Test suite for Pydantic schema validation"""

    def test_product_create_valid_data(self):
        """Test ProductCreate accepts all valid data types and structures"""
        valid_product_data = {
            "product_name": "Gaming Laptop",
            "category": ["electronics", "computers"],
            "discounted_price": 799.99,
            "actual_price": 999.99,
            "discount_percentage": "20%",
            "rating": 4.5,
            "rating_count": 150,
            "about_product": "High-performance gaming laptop with RGB keyboard",
            "user_id": ["user123", "user456"],
            "user_name": ["John Doe", "Jane Smith"],
            "review_id": ["rev1", "rev2"],
            "review_title": ["Great laptop!", "Excellent performance"],
            "review_content": "Amazing gaming experience with this laptop.",
            "img_link": "https://example.com/laptop.jpg",
            "product_link": "https://example.com/products/gaming-laptop"
        }
        
        product = ProductCreate(**valid_product_data)
        
        # Verify all fields are correctly assigned
        assert product.product_name == "Gaming Laptop"
        assert product.category == ["electronics", "computers"]
        assert product.discounted_price == 799.99
        assert product.actual_price == 999.99
        assert product.rating == 4.5
        assert product.rating_count == 150
        assert len(product.user_id) == 2
        assert len(product.review_title) == 2

    def test_user_create_valid_data_with_constraints(self):
        """Test UserCreate validates email format and field length constraints"""
        valid_user_data = {
            "username": "testuser123",
            "email": "testuser@example.com",
            "password": "securePassword123!"
        }
        
        user = UserCreate(**valid_user_data)
        
        assert user.username == "testuser123"
        assert user.email == "testuser@example.com"
        assert user.password == "securePassword123!"
        
        # Test boundary values for constraints
        min_username = UserCreate(
            username="abc",  # Minimum 3 characters
            email="test@example.com",
            password="12345678"  # Minimum 8 characters
        )
        assert min_username.username == "abc"
        assert min_username.password == "12345678"

    def test_product_create_invalid_data_types(self):
        """Test ProductCreate rejects invalid data types"""
        
        # Test invalid price (string instead of float)
        with pytest.raises(ValidationError) as exc_info:
            ProductCreate(
                product_name="Test Product",
                discounted_price="not_a_number",  # Should be float
                actual_price=100.0,
                discount_percentage="10%",
                rating=4.0,
                rating_count=50,
                about_product="Test description",
                review_content="Test review",
                img_link="http://test.com",
                product_link="http://test.com"
            )
        
        errors = exc_info.value.errors()
        assert any("Input should be a valid number" in str(error) for error in errors)
        
        # Test invalid rating_count (float instead of int)
        with pytest.raises(ValidationError) as exc_info:
            ProductCreate(
                product_name="Test Product",
                discounted_price=50.0,
                actual_price=100.0,
                discount_percentage="10%",
                rating=4.0,
                rating_count=50.5,  # Should be int
                about_product="Test description",
                review_content="Test review",
                img_link="http://test.com",
                product_link="http://test.com"
            )
        
        errors = exc_info.value.errors()
        assert any("Input should be a valid integer" in str(error) for error in errors)

    def test_user_create_validation_constraints(self):
        """Test UserCreate enforces field constraints and email validation"""
        
        # Test username too short (less than 3 characters)
        with pytest.raises(ValidationError) as exc_info:
            UserCreate(
                username="ab",  # Too short
                email="test@example.com",
                password="validPassword123"
            )
        
        errors = exc_info.value.errors()
        assert any("at least 3 characters" in str(error) for error in errors)
        
        # Test password too short (less than 8 characters)
        with pytest.raises(ValidationError) as exc_info:
            UserCreate(
                username="validuser",
                email="test@example.com",
                password="short"  # Too short
            )
        
        errors = exc_info.value.errors()
        assert any("at least 8 characters" in str(error) for error in errors)
        
        # Test invalid email format
        with pytest.raises(ValidationError) as exc_info:
            UserCreate(
                username="validuser",
                email="not_an_email",  # Invalid email format
                password="validPassword123"
            )
        
        errors = exc_info.value.errors()
        assert any("value is not a valid email address" in str(error) for error in errors)

    def test_product_preview_validation_lightweight_schema(self):
        """Test ProductPreview validates lightweight product data correctly"""
        
        # Test valid ProductPreview data
        valid_preview_data = {
            "product_id": "prod123",
            "product_name": "Wireless Mouse",
            "discounted_price": 25.99,
            "rating": 4.3
        }
        
        preview = ProductPreview(**valid_preview_data)
        
        assert preview.product_id == "prod123"
        assert preview.product_name == "Wireless Mouse"
        assert preview.discounted_price == 25.99
        assert preview.rating == 4.3
        
        # Test missing required field
        with pytest.raises(ValidationError) as exc_info:
            ProductPreview(
                product_id="prod123",
                product_name="Wireless Mouse",
                # Missing discounted_price and rating
            )
        
        errors = exc_info.value.errors()
        assert len(errors) >= 2  # Should have errors for missing fields
        
        # Test invalid data type for rating
        with pytest.raises(ValidationError) as exc_info:
            ProductPreview(
                product_id="prod123",
                product_name="Wireless Mouse",
                discounted_price=25.99,
                rating="four_stars"  # Should be float
            )
        
        errors = exc_info.value.errors()
        assert any("Input should be a valid number" in str(error) for error in errors)
