"""
Test Suite for User Registration Functionality

This module contains comprehensive tests for user registration including:
- Successful user creation with valid data
- Duplicate email prevention and validation
- Duplicate username prevention and validation
- Data persistence and structure validation
- Edge cases and input validation

Author: BEIJ Team
Date: November 2024
PR: #2 - User Registration Tests
"""

import pytest
from unittest.mock import patch, MagicMock
from fastapi import HTTPException
import uuid

from app.services.user_service import create_user, hash_password
from app.schemas.user import UserCreate, UserResponse


class TestUserRegistration:
    """Test user registration functionality"""
    
    @patch('app.services.user_service.load_all')
    @patch('app.services.user_service.save_all')
    @patch('uuid.uuid4')
    def test_create_user_success(self, mock_uuid, mock_save, mock_load):
        """Test successful user creation with valid data"""
        # Mock empty user database
        mock_load.return_value = []
        mock_uuid.return_value = MagicMock()
        mock_uuid.return_value.__str__ = MagicMock(return_value="test-uuid-123")
        
        user_create = UserCreate(
            username="newuser",
            email="newuser@example.com",
            password="securePassword123"
        )
        
        result = create_user(user_create)
        
        # Should return UserResponse with correct data
        assert isinstance(result, UserResponse)
        assert result.username == "newuser"
        assert result.email == "newuser@example.com"
        assert result.user_id == "test-uuid-123"
        
        # Should call save_all once to persist user
        mock_save.assert_called_once()
        
        # Verify the saved data structure
        saved_data = mock_save.call_args[0][0]
        assert len(saved_data) == 1
        assert saved_data[0]["username"] == "newuser"
        assert saved_data[0]["email"] == "newuser@example.com"
        assert saved_data[0]["user_id"] == "test-uuid-123"
        assert "hashed_password" in saved_data[0]
        assert saved_data[0]["hashed_password"] != "securePassword123"  # Should be hashed
    
    @patch('app.services.user_service.load_all')
    def test_create_user_duplicate_email(self, mock_load):
        """Test user creation fails with duplicate email"""
        # Mock existing user with same email
        mock_load.return_value = [
            {
                "user_id": "existing-user-id",
                "username": "existinguser",
                "email": "duplicate@example.com",
                "hashed_password": "hashedpassword"
            }
        ]
        
        user_create = UserCreate(
            username="newuser",
            email="duplicate@example.com",  # Duplicate email
            password="password123"
        )
        
        # Should raise HTTPException with 409 status
        with pytest.raises(HTTPException) as exc_info:
            create_user(user_create)
        
        assert exc_info.value.status_code == 409
        assert "Email already exists" in str(exc_info.value.detail)
    
    @patch('app.services.user_service.load_all')
    def test_create_user_duplicate_username(self, mock_load):
        """Test user creation fails with duplicate username"""
        # Mock existing user with same username
        mock_load.return_value = [
            {
                "user_id": "existing-user-id",
                "username": "duplicateuser",
                "email": "existing@example.com",
                "hashed_password": "hashedpassword"
            }
        ]
        
        user_create = UserCreate(
            username="duplicateuser",  # Duplicate username
            email="new@example.com",
            password="password123"
        )
        
        # Should raise HTTPException with 409 status
        with pytest.raises(HTTPException) as exc_info:
            create_user(user_create)
        
        assert exc_info.value.status_code == 409
        assert "Username already exists" in str(exc_info.value.detail)
    
    @patch('app.services.user_service.load_all')
    def test_create_user_case_sensitive_username(self, mock_load):
        """Test that usernames are case sensitive"""
        # Mock existing user
        mock_load.return_value = [
            {
                "user_id": "existing-user-id",
                "username": "TestUser",
                "email": "existing@example.com",
                "hashed_password": "hashedpassword"
            }
        ]
        
        # Different case should be allowed
        user_create = UserCreate(
            username="testuser",  # Different case
            email="new@example.com",
            password="password123"
        )
        
        # Should not raise exception (usernames are case sensitive)
        # This test verifies current behavior - you might want case-insensitive usernames
        with patch('app.services.user_service.save_all'):
            result = create_user(user_create)
            assert result.username == "testuser"
    
    @patch('app.services.user_service.load_all')
    def test_create_user_case_sensitive_email_current_behavior(self, mock_load):
        """Test current behavior: emails are case sensitive"""
        # Mock existing user with lowercase email
        mock_load.return_value = [
            {
                "user_id": "existing-user-id",
                "username": "existinguser",
                "email": "test@example.com",  # lowercase
                "hashed_password": "hashedpassword"
            }
        ]
        
        # Try to create user with uppercase email
        user_create = UserCreate(
            username="newuser",
            email="TEST@EXAMPLE.COM",  # uppercase - different case
            password="password123"
        )
        
        # Current behavior: Pydantic EmailStr normalizes emails to lowercase
        # So "TEST@EXAMPLE.COM" becomes "TEST@example.com"
        with patch('app.services.user_service.save_all'):
            result = create_user(user_create)
            assert result.email == "TEST@example.com"  # Domain normalized to lowercase
            assert result.username == "newuser"
    
    @patch('app.services.user_service.load_all')
    @patch('app.services.user_service.save_all')
    def test_create_user_password_is_hashed(self, mock_save, mock_load):
        """Test that user passwords are properly hashed before storage"""
        mock_load.return_value = []
        
        original_password = "myPlainTextPassword123"
        user_create = UserCreate(
            username="testuser",
            email="test@example.com",
            password=original_password
        )
        
        result = create_user(user_create)
        
        # Verify password was hashed
        saved_data = mock_save.call_args[0][0]
        stored_password = saved_data[0]["hashed_password"]
        
        # Stored password should not be the original
        assert stored_password != original_password
        # Stored password should be a bcrypt hash (starts with $2b$)
        assert stored_password.startswith("$2b$")
        # Should be reasonable length for bcrypt hash
        assert 50 < len(stored_password) < 100
    
    @patch('app.services.user_service.load_all')
    @patch('app.services.user_service.save_all')
    def test_create_user_username_trimmed(self, mock_save, mock_load):
        """Test that usernames are trimmed of whitespace"""
        mock_load.return_value = []
        
        user_create = UserCreate(
            username="  spaceduser  ",  # Username with spaces
            email="test@example.com",
            password="password123"
        )
        
        result = create_user(user_create)
        
        # Username should be trimmed in response
        assert result.username == "spaceduser"
        
        # Username should be trimmed in saved data
        saved_data = mock_save.call_args[0][0]
        assert saved_data[0]["username"] == "spaceduser"
    
    @patch('app.services.user_service.load_all')
    @patch('app.services.user_service.save_all')
    def test_create_user_multiple_users_database(self, mock_save, mock_load):
        """Test creating user when database already has other users"""
        # Mock existing users in database
        mock_load.return_value = [
            {
                "user_id": "user1",
                "username": "existinguser1",
                "email": "user1@example.com",
                "hashed_password": "hash1"
            },
            {
                "user_id": "user2",
                "username": "existinguser2", 
                "email": "user2@example.com",
                "hashed_password": "hash2"
            }
        ]
        
        user_create = UserCreate(
            username="newuser",
            email="newuser@example.com",
            password="password123"
        )
        
        result = create_user(user_create)
        
        # Should successfully create new user
        assert result.username == "newuser"
        assert result.email == "newuser@example.com"
        
        # Should save all users (existing + new)
        saved_data = mock_save.call_args[0][0]
        assert len(saved_data) == 3  # 2 existing + 1 new
        
        # New user should be appended to the list
        new_user = saved_data[2]
        assert new_user["username"] == "newuser"
        assert new_user["email"] == "newuser@example.com"
    
    def test_create_user_with_minimum_valid_data(self):
        """Test creating user with minimum required fields"""
        # Test that UserCreate schema accepts minimum valid data
        user_create = UserCreate(
            username="min",  # Minimum 3 characters
            email="a@b.co",  # Minimum valid email
            password="12345678"  # Minimum 8 characters
        )
        
        # Should create UserCreate object successfully
        assert user_create.username == "min"
        assert user_create.email == "a@b.co"
        assert user_create.password == "12345678"
    
    def test_create_user_validation_errors(self):
        """Test that invalid user data raises validation errors"""
        from pydantic import ValidationError
        
        # Test username too short
        with pytest.raises(ValidationError) as exc_info:
            UserCreate(
                username="ab",  # Too short (minimum 3)
                email="test@example.com",
                password="password123"
            )
        assert "at least 3 characters" in str(exc_info.value)
        
        # Test username too long
        with pytest.raises(ValidationError) as exc_info:
            UserCreate(
                username="a" * 51,  # Too long (maximum 50)
                email="test@example.com", 
                password="password123"
            )
        assert "at most 50 characters" in str(exc_info.value)
        
        # Test invalid email format
        with pytest.raises(ValidationError) as exc_info:
            UserCreate(
                username="testuser",
                email="invalid-email",  # Invalid format
                password="password123"
            )
        assert "value is not a valid email address" in str(exc_info.value)
        
        # Test password too short
        with pytest.raises(ValidationError) as exc_info:
            UserCreate(
                username="testuser",
                email="test@example.com",
                password="1234567"  # Too short (minimum 8)
            )
        assert "at least 8 characters" in str(exc_info.value)
