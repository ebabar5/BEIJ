"""
Test Suite for Password Security Functionality

This module contains comprehensive tests for password hashing and verification security:
- Password hashing creates different hashes each time (salt randomization)
- Password verification works correctly
- Password security with special characters and unicode
- Long password handling (bcrypt 72-char limit)
- Security requirements validation

Author: BEIJ Team
Date: November 2024
PR: #1 - Password Security Tests
"""

import pytest
from app.services.user_service import hash_password, verify_password


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
