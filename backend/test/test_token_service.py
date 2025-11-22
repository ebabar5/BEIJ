import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta
from fastapi import HTTPException
import jwt
from app.services.token_service import (
    generate_token,
    verify_token,
    invalidate_token,
    invalidate_user_tokens,
    SECRET_KEY,
    ALGORITHM,
    REGULAR_TOKEN_EXPIRY_HOURS,
    REMEMBER_ME_TOKEN_EXPIRY_DAYS
)


class TestTokenService:
    
    @patch('app.services.token_service.add_token')
    @patch('app.services.token_service.remove_expired_tokens')
    @patch('app.services.token_service.datetime')
    def test_generate_token_regular_expiration(self, mock_datetime, mock_remove_expired, mock_add_token):
        mock_now = datetime(2030, 1, 1, 12, 0, 0)
        mock_datetime.utcnow.return_value = mock_now
        mock_datetime.side_effect = lambda *args, **kw: datetime(*args, **kw)
        
        result = generate_token("user123", "testuser", "test@example.com", remember_me=False, is_admin=False)
        
        assert "token" in result
        assert "expires_at" in result
        assert "expires_in" in result
        assert result["expires_in"] == REGULAR_TOKEN_EXPIRY_HOURS * 3600
        
        expected_expires = mock_now + timedelta(hours=REGULAR_TOKEN_EXPIRY_HOURS)
        assert result["expires_at"] == expected_expires.isoformat()
        
        decoded = jwt.decode(result["token"], SECRET_KEY, algorithms=[ALGORITHM], options={"verify_exp": False, "verify_iat": False})
        assert decoded["user_id"] == "user123"
        assert decoded["username"] == "testuser"
        assert decoded["email"] == "test@example.com"
        assert decoded["remember_me"] is False
        assert decoded["is_admin"] is False
    
    @patch('app.services.token_service.add_token')
    @patch('app.services.token_service.remove_expired_tokens')
    @patch('app.services.token_service.datetime')
    def test_generate_token_remember_me_expiration(self, mock_datetime, mock_remove_expired, mock_add_token):
        mock_now = datetime(2030, 1, 1, 12, 0, 0)
        mock_datetime.utcnow.return_value = mock_now
        mock_datetime.side_effect = lambda *args, **kw: datetime(*args, **kw)
        
        result = generate_token("user123", "testuser", "test@example.com", remember_me=True, is_admin=False)
        
        assert result["expires_in"] == REMEMBER_ME_TOKEN_EXPIRY_DAYS * 24 * 3600
        
        expected_expires = mock_now + timedelta(days=REMEMBER_ME_TOKEN_EXPIRY_DAYS)
        assert result["expires_at"] == expected_expires.isoformat()
        
        decoded = jwt.decode(result["token"], SECRET_KEY, algorithms=[ALGORITHM], options={"verify_exp": False, "verify_iat": False})
        assert decoded["remember_me"] is True
    
    @patch('app.services.token_service.add_token')
    @patch('app.services.token_service.remove_expired_tokens')
    @patch('app.services.token_service.datetime')
    def test_generate_token_with_admin_flag(self, mock_datetime, mock_remove_expired, mock_add_token):
        mock_now = datetime(2030, 1, 1, 12, 0, 0)
        mock_datetime.utcnow.return_value = mock_now
        mock_datetime.side_effect = lambda *args, **kw: datetime(*args, **kw)
        
        result = generate_token("admin123", "adminuser", "admin@example.com", remember_me=False, is_admin=True)
        
        decoded = jwt.decode(result["token"], SECRET_KEY, algorithms=[ALGORITHM], options={"verify_exp": False, "verify_iat": False})
        assert decoded["is_admin"] is True
        assert decoded["user_id"] == "admin123"
    
    @patch('app.services.token_service.add_token')
    @patch('app.services.token_service.remove_expired_tokens')
    @patch('app.services.token_service.datetime')
    def test_generate_token_stores_token_data(self, mock_datetime, mock_remove_expired, mock_add_token):
        mock_now = datetime(2030, 1, 1, 12, 0, 0)
        mock_datetime.utcnow.return_value = mock_now
        mock_datetime.side_effect = lambda *args, **kw: datetime(*args, **kw)
        
        result = generate_token("user123", "testuser", "test@example.com", remember_me=False, is_admin=False)
        
        mock_add_token.assert_called_once()
        call_args = mock_add_token.call_args[0][0]
        assert call_args["token"] == result["token"]
        assert call_args["user_id"] == "user123"
        assert call_args["remember_me"] is False
        assert "expires_at" in call_args
        assert "created_at" in call_args
    
    @patch('app.services.token_service.get_token')
    @patch('app.services.token_service.add_token')
    @patch('app.services.token_service.remove_expired_tokens')
    @patch('app.services.token_service.datetime')
    def test_verify_token_success(self, mock_datetime, mock_remove_expired, mock_add_token, mock_get_token):
        real_now = datetime.utcnow()
        future_time = real_now + timedelta(days=1)
        mock_datetime.utcnow.return_value = real_now
        mock_datetime.fromisoformat.return_value = future_time
        mock_datetime.side_effect = lambda *args, **kw: datetime(*args, **kw)
        
        token_result = generate_token("user123", "testuser", "test@example.com", remember_me=False, is_admin=False)
        token = token_result["token"]
        
        mock_get_token.return_value = {
            "token": token,
            "user_id": "user123",
            "expires_at": token_result["expires_at"],
            "remember_me": False
        }
        
        result = verify_token(token)
        
        assert result["user_id"] == "user123"
        assert result["username"] == "testuser"
        assert result["email"] == "test@example.com"
    
    @patch('app.services.token_service.get_token')
    def test_verify_token_not_found(self, mock_get_token):
        mock_get_token.return_value = None
        
        with pytest.raises(HTTPException) as exc_info:
            verify_token("invalid-token")
        
        assert exc_info.value.status_code == 401
        assert "Token not found or invalid" in str(exc_info.value.detail)
    
    @patch('app.services.token_service.get_token')
    @patch('app.services.token_service.remove_token')
    @patch('app.services.token_service.datetime')
    def test_verify_token_expired(self, mock_datetime, mock_remove_token, mock_get_token):
        mock_now = datetime(2030, 1, 1, 12, 0, 0)
        past_time = mock_now - timedelta(hours=1)
        mock_datetime.utcnow.return_value = mock_now
        mock_datetime.fromisoformat.return_value = past_time
        mock_datetime.side_effect = lambda *args, **kw: datetime(*args, **kw)
        
        token = jwt.encode({
            "user_id": "user123",
            "exp": int(past_time.timestamp()),
            "iat": int(past_time.timestamp())
        }, SECRET_KEY, algorithm=ALGORITHM)
        
        mock_get_token.return_value = {
            "token": token,
            "expires_at": past_time.isoformat()
        }
        
        with pytest.raises(HTTPException) as exc_info:
            verify_token(token)
        
        assert exc_info.value.status_code == 401
        assert "Token has expired" in str(exc_info.value.detail)
        mock_remove_token.assert_called_once_with(token)
    
    @patch('app.services.token_service.get_token')
    @patch('app.services.token_service.remove_token')
    @patch('app.services.token_service.datetime')
    def test_verify_token_invalid_jwt(self, mock_datetime, mock_remove_token, mock_get_token):
        future_time = datetime(2030, 1, 1, 13, 0, 0)
        mock_datetime.utcnow.return_value = datetime(2030, 1, 1, 12, 0, 0)
        mock_datetime.fromisoformat.return_value = future_time
        mock_datetime.side_effect = lambda *args, **kw: datetime(*args, **kw)
        
        mock_get_token.return_value = {
            "token": "invalid-jwt-token",
            "expires_at": future_time.isoformat()
        }
        
        with pytest.raises(HTTPException) as exc_info:
            verify_token("invalid-jwt-token")
        
        assert exc_info.value.status_code == 401
        assert "Invalid token" in str(exc_info.value.detail)
    
    @patch('app.services.token_service.get_token')
    @patch('app.services.token_service.remove_token')
    @patch('app.services.token_service.datetime')
    def test_verify_token_jwt_expired_signature(self, mock_datetime, mock_remove_token, mock_get_token):
        real_now = datetime.utcnow()
        past_time = real_now - timedelta(hours=1)
        mock_datetime.utcnow.return_value = real_now
        mock_datetime.fromisoformat.return_value = past_time
        mock_datetime.side_effect = lambda *args, **kw: datetime(*args, **kw)
        
        expired_token = jwt.encode({
            "user_id": "user123",
            "exp": int(past_time.timestamp()),
            "iat": int((past_time - timedelta(hours=1)).timestamp())
        }, SECRET_KEY, algorithm=ALGORITHM)
        
        mock_get_token.return_value = {
            "token": expired_token,
            "expires_at": past_time.isoformat()
        }
        
        with pytest.raises(HTTPException) as exc_info:
            verify_token(expired_token)
        
        assert exc_info.value.status_code == 401
        assert "Token has expired" in str(exc_info.value.detail)
        mock_remove_token.assert_called_once_with(expired_token)
    
    @patch('app.services.token_service.remove_token')
    def test_invalidate_token_success(self, mock_remove_token):
        invalidate_token("test-token-123")
        
        mock_remove_token.assert_called_once_with("test-token-123")
    
    @patch('app.services.token_service.remove_user_tokens')
    def test_invalidate_user_tokens_success(self, mock_remove_user_tokens):
        invalidate_user_tokens("user123")
        
        mock_remove_user_tokens.assert_called_once_with("user123")
    
    @patch('app.services.token_service.add_token')
    @patch('app.services.token_service.remove_expired_tokens')
    @patch('app.services.token_service.datetime')
    def test_generate_token_calls_remove_expired(self, mock_datetime, mock_remove_expired, mock_add_token):
        mock_now = datetime(2030, 1, 1, 12, 0, 0)
        mock_datetime.utcnow.return_value = mock_now
        mock_datetime.side_effect = lambda *args, **kw: datetime(*args, **kw)
        
        generate_token("user123", "testuser", "test@example.com")
        
        mock_remove_expired.assert_called_once()

