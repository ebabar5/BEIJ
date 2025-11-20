"""
Test Suite for User Authentication Functionality

This module contains comprehensive tests for user authentication including:
- User registration
- Password hashing and verification  
- User login with username/email
- Authentication error handling
- Security validation

Author: BEIJ Team
Date: November 2024
"""

import pytest
from unittest.mock import patch, MagicMock
from fastapi import HTTPException
import uuid

from app.services.user_service import (
    create_user, 
    authenticate_user, 
    hash_password, 
    verify_password,
    list_users
)
from app.schemas.user import UserCreate, UserLogin, UserResponse


class TestPasswordSecurity:
    """Test password hashing and verification security"""
    
    def test_hash_password_creates_different_hash_each_time(self):
        """Test that hashing the same password twice creates different hashes"""
        password = "testpassword123"
        hash1 = hash_password(password)
        hash2 = hash_password(password)
        
        # Hashes should be different (due to random salt)
        assert hash1 != hash2
        # Both should verify correctly
        assert verify_password(password, hash1)
        assert verify_password(password, hash2)
    
    def test_hash_password_basic_functionality(self):
        """Test basic password hashing functionality"""
        password = "mySecurePassword123!"
        hashed = hash_password(password)
        
        # Hash should be different from original password
        assert hashed != password
        # Hash should be a string
        assert isinstance(hashed, str)
        # Hash should have reasonable length (bcrypt hashes are ~60 chars)
        assert len(hashed) > 50
        assert len(hashed) < 100
    
    def test_verify_password_correct_password(self):
        """Test password verification with correct password"""
        password = "correctPassword123"
        hashed = hash_password(password)
        
        # Correct password should verify successfully
        assert verify_password(password, hashed) is True
    
    def test_verify_password_incorrect_password(self):
        """Test password verification with incorrect password"""
        correct_password = "correctPassword123"
        wrong_password = "wrongPassword456"
        hashed = hash_password(correct_password)
        
        # Wrong password should fail verification
        assert verify_password(wrong_password, hashed) is False
    
    def test_verify_password_empty_password(self):
        """Test password verification with empty password"""
        password = "testPassword"
        hashed = hash_password(password)
        
        # Empty password should fail verification
        assert verify_password("", hashed) is False
    
    def test_hash_password_long_password(self):
        """Test password hashing with very long password (>72 chars)"""
        # bcrypt has 72 character limit, test our truncation
        long_password = "a" * 100  # 100 character password
        hashed = hash_password(long_password)
        
        # Should still work and be verifiable
        assert verify_password(long_password, hashed) is True
        
        # Should also work with exactly 72 chars
        password_72 = "a" * 72
        assert verify_password(password_72, hashed) is True
    
    def test_hash_password_special_characters(self):
        """Test password hashing with special characters"""
        special_password = "P@ssw0rd!#$%^&*()_+-=[]{}|;:,.<>?"
        hashed = hash_password(special_password)
        
        assert verify_password(special_password, hashed) is True
    
    def test_hash_password_unicode_characters(self):
        """Test password hashing with unicode characters"""
        unicode_password = "пароль123🔐"
        hashed = hash_password(unicode_password)
        
        assert verify_password(unicode_password, hashed) is True


class TestUserRegistration:
    """Test user registration functionality"""
    
    @patch('app.services.user_service.load_all')
    @patch('app.services.user_service.save_all')
    @patch('uuid.uuid4')
    def test_create_user_success(self, mock_uuid, mock_save, mock_load):
        """Test successful user creation"""
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
        assert "username already exists" in str(exc_info.value.detail)
    
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


class TestUserAuthentication:
    """Test user login and authentication"""
    
    @patch('app.services.user_service.load_all')
    def test_authenticate_user_with_username_success(self, mock_load):
        """Test successful authentication using username"""
        # Create a test password and hash it
        test_password = "myTestPassword123"
        hashed_password = hash_password(test_password)
        
        # Mock user database
        mock_load.return_value = [
            {
                "user_id": "test-user-id",
                "username": "testuser",
                "email": "test@example.com",
                "hashed_password": hashed_password
            }
        ]
        
        # Test login with username
        user_login = UserLogin(
            username_or_email="testuser",
            password=test_password
        )
        
        result = authenticate_user(user_login)
        
        # Should return UserResponse with correct data
        assert isinstance(result, UserResponse)
        assert result.username == "testuser"
        assert result.email == "test@example.com"
        assert result.user_id == "test-user-id"
    
    @patch('app.services.user_service.load_all')
    def test_authenticate_user_with_email_success(self, mock_load):
        """Test successful authentication using email"""
        test_password = "myTestPassword123"
        hashed_password = hash_password(test_password)
        
        mock_load.return_value = [
            {
                "user_id": "test-user-id",
                "username": "testuser",
                "email": "test@example.com",
                "hashed_password": hashed_password
            }
        ]
        
        # Test login with email instead of username
        user_login = UserLogin(
            username_or_email="test@example.com",
            password=test_password
        )
        
        result = authenticate_user(user_login)
        
        assert isinstance(result, UserResponse)
        assert result.username == "testuser"
        assert result.email == "test@example.com"
        assert result.user_id == "test-user-id"
    
    @patch('app.services.user_service.load_all')
    def test_authenticate_user_not_found(self, mock_load):
        """Test authentication with non-existent user"""
        # Mock empty user database
        mock_load.return_value = []
        
        user_login = UserLogin(
            username_or_email="nonexistentuser",
            password="anypassword"
        )
        
        # Should raise HTTPException with 401 status
        with pytest.raises(HTTPException) as exc_info:
            authenticate_user(user_login)
        
        assert exc_info.value.status_code == 401
        assert "Invalid credentials" in str(exc_info.value.detail)
    
    @patch('app.services.user_service.load_all')
    def test_authenticate_user_wrong_password(self, mock_load):
        """Test authentication with incorrect password"""
        correct_password = "correctPassword123"
        wrong_password = "wrongPassword456"
        hashed_password = hash_password(correct_password)
        
        mock_load.return_value = [
            {
                "user_id": "test-user-id",
                "username": "testuser",
                "email": "test@example.com",
                "hashed_password": hashed_password
            }
        ]
        
        user_login = UserLogin(
            username_or_email="testuser",
            password=wrong_password
        )
        
        # Should raise HTTPException with 401 status
        with pytest.raises(HTTPException) as exc_info:
            authenticate_user(user_login)
        
        assert exc_info.value.status_code == 401
        assert "invalid credentials" in str(exc_info.value.detail)
    
    def test_authenticate_user_empty_password_validation(self):
        """Test that empty password is rejected by Pydantic validation"""
        # Empty password should be rejected by Pydantic validation before reaching service
        from pydantic import ValidationError
        
        with pytest.raises(ValidationError) as exc_info:
            UserLogin(
                username_or_email="testuser",
                password=""  # Empty password - should fail validation
            )
        
        # Should fail validation due to minimum length requirement
        assert "String should have at least 8 characters" in str(exc_info.value)
    
    @patch('app.services.user_service.load_all')
    def test_authenticate_user_case_sensitivity(self, mock_load):
        """Test authentication case sensitivity"""
        test_password = "testPassword123"
        hashed_password = hash_password(test_password)
        
        mock_load.return_value = [
            {
                "user_id": "test-user-id",
                "username": "TestUser",
                "email": "Test@Example.com",
                "hashed_password": hashed_password
            }
        ]
        
        # Test with different case username (should fail)
        user_login = UserLogin(
            username_or_email="testuser",  # Different case
            password=test_password
        )
        
        with pytest.raises(HTTPException) as exc_info:
            authenticate_user(user_login)
        
        assert exc_info.value.status_code == 401


class TestUserManagement:
    """Test user management functionality"""
    
    @patch('app.services.user_service.load_all')
    def test_list_users_empty_database(self, mock_load):
        """Test listing users when database is empty"""
        mock_load.return_value = []
        
        result = list_users()
        
        assert result == []
        assert isinstance(result, list)
    
    @patch('app.services.user_service.load_all')
    def test_list_users_with_data(self, mock_load):
        """Test listing users with data in database"""
        mock_load.return_value = [
            {
                "user_id": "user1",
                "username": "user1",
                "email": "user1@example.com",
                "hashed_password": "hash1"
            },
            {
                "user_id": "user2",
                "username": "user2", 
                "email": "user2@example.com",
                "hashed_password": "hash2"
            }
        ]
        
        result = list_users()
        
        # Should return list of UserResponse objects
        assert len(result) == 2
        assert all(isinstance(user, UserResponse) for user in result)
        
        # Check first user
        assert result[0].user_id == "user1"
        assert result[0].username == "user1"
        assert result[0].email == "user1@example.com"
        
        # Check second user
        assert result[1].user_id == "user2"
        assert result[1].username == "user2"
        assert result[1].email == "user2@example.com"
        
        # Should not include hashed_password in response
        assert not hasattr(result[0], 'hashed_password')
        assert not hasattr(result[1], 'hashed_password')


class TestAuthenticationEdgeCases:
    """Test edge cases and security scenarios"""
    
    @patch('app.services.user_service.load_all')
    def test_authenticate_user_multiple_users_same_email(self, mock_load):
        """Test authentication when multiple users have same email (edge case)"""
        # This shouldn't happen in normal operation, but test the behavior
        test_password = "password123"
        hashed_password = hash_password(test_password)
        
        mock_load.return_value = [
            {
                "user_id": "user1",
                "username": "user1",
                "email": "shared@example.com",
                "hashed_password": hashed_password
            },
            {
                "user_id": "user2",
                "username": "user2",
                "email": "shared@example.com",  # Same email
                "hashed_password": hashed_password
            }
        ]
        
        user_login = UserLogin(
            username_or_email="shared@example.com",
            password=test_password
        )
        
        # Should authenticate with the first matching user
        result = authenticate_user(user_login)
        assert result.user_id == "user1"  # First user found
    
    def test_password_security_requirements(self):
        """Test that password hashing meets security requirements"""
        password = "testPassword123"
        hash1 = hash_password(password)
        hash2 = hash_password(password)
        
        # Hashes should be different (salt randomization)
        assert hash1 != hash2
        
        # Both should verify correctly
        assert verify_password(password, hash1)
        assert verify_password(password, hash2)
        
        # Hash should not contain original password
        assert password not in hash1
        assert password not in hash2
        
        # Hash should be reasonable length
        assert 50 < len(hash1) < 100
        assert 50 < len(hash2) < 100
