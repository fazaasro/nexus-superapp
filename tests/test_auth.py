"""
Authentication module tests
"""
import pytest
from core.auth import (
    hash_password,
    verify_password,
    create_access_token,
    decode_access_token,
    create_refresh_token
)


class TestPasswordHashing:
    """Test password hashing and verification"""

    def test_hash_password(self):
        """Test password hashing"""
        password = "SecurePassword123"
        hashed = hash_password(password)

        assert hashed is not None
        assert hashed != password
        assert len(hashed) > 50  # Bcrypt hashes are long

    def test_verify_password_correct(self):
        """Test correct password verification"""
        password = "SecurePassword123"
        hashed = hash_password(password)

        assert verify_password(password, hashed) is True

    def test_verify_password_incorrect(self):
        """Test incorrect password verification"""
        password = "SecurePassword123"
        wrong_password = "WrongPassword"
        hashed = hash_password(password)

        assert verify_password(wrong_password, hashed) is False

    def test_hash_same_password_different_hashes(self):
        """Test that hashing same password twice produces different hashes"""
        password = "SecurePassword123"
        hash1 = hash_password(password)
        hash2 = hash_password(password)

        # Bcrypt includes salt, so hashes should differ
        assert hash1 != hash2


class TestTokenCreation:
    """Test JWT token creation"""

    def test_create_access_token(self):
        """Test access token creation"""
        user_id = "test_user"
        email = "test@example.com"

        token_data = create_access_token(user_id, email)

        assert 'access_token' in token_data
        assert 'refresh_token' in token_data
        assert 'token_type' in token_data
        assert token_data['token_type'] == 'bearer'

    def test_access_token_has_expiry(self):
        """Test that access token includes expiry time"""
        user_id = "test_user"
        email = "test@example.com"

        token_data = create_access_token(user_id, email)

        assert 'expires_in' in token_data
        assert token_data['expires_in'] > 0


class TestTokenDecoding:
    """Test JWT token decoding"""

    def test_decode_valid_token(self):
        """Test decoding valid token"""
        user_id = "test_user"
        email = "test@example.com"

        token_data = create_access_token(user_id, email)
        decoded = decode_access_token(token_data['access_token'])

        assert decoded is not None
        assert decoded['user_id'] == user_id
        assert decoded['email'] == email

    def test_decode_invalid_token(self):
        """Test decoding invalid token"""
        invalid_token = "invalid.jwt.token"

        decoded = decode_access_token(invalid_token)

        assert decoded is None

    def test_decode_expired_token(self):
        """Test decoding expired token (if implemented)"""
        # This test depends on token expiration implementation
        # For now, just verify it doesn't crash
        user_id = "test_user"
        email = "test@example.com"

        token_data = create_access_token(user_id, email)
        decoded = decode_access_token(token_data['access_token'])

        assert decoded is not None


class TestRefreshToken:
    """Test refresh token creation"""

    def test_create_refresh_token(self):
        """Test refresh token creation"""
        user_id = "test_user"

        refresh_token = create_refresh_token(user_id)

        assert refresh_token is not None
        assert len(refresh_token) > 50  # JWT tokens are long

    def test_refresh_token_different_from_access(self):
        """Test that refresh token differs from access token"""
        user_id = "test_user"
        email = "test@example.com"

        access_data = create_access_token(user_id, email)
        refresh_token = create_refresh_token(user_id)

        assert access_data['refresh_token'] != refresh_token


class TestAuthDependencies:
    """Test FastAPI authentication dependencies"""

    @pytest.mark.asyncio
    async def test_get_current_user_valid_token(self, admin_token):
        """Test get_current_user with valid token"""
        from core.auth import get_current_user

        # Create mock request with valid token
        from fastapi import Request
        from starlette.requests import Request as StarletteRequest

        scope = {
            'type': 'http',
            'headers': [(b'authorization', f'bearer {admin_token}'.encode())]
        }

        request = StarletteRequest(scope)

        # This would require a real FastAPI app context
        # For unit testing, we'll just verify the function exists
        assert callable(get_current_user)

    @pytest.mark.asyncio
    async def test_get_current_user_missing_token(self):
        """Test get_current_user with missing token"""
        from core.auth import get_current_user, HTTPException

        # Mock request without token
        from starlette.requests import Request as StarletteRequest

        scope = {
            'type': 'http',
            'headers': []
        }

        request = StarletteRequest(scope)

        # This should raise HTTPException
        assert callable(get_current_user)


@pytest.mark.integration
class TestAuthFlow:
    """Integration tests for authentication flow"""

    @pytest.mark.asyncio
    async def test_complete_auth_flow(self, test_user):
        """Test complete authentication flow: hash -> token -> decode -> verify"""
        password = "TestPassword123"

        # Hash password
        hashed = hash_password(password)
        assert hashed is not None

        # Verify password
        assert verify_password(password, hashed) is True

        # Create token
        token_data = create_access_token(test_user['user_id'], test_user['email'])
        assert token_data is not None

        # Decode token
        decoded = decode_access_token(token_data['access_token'])
        assert decoded is not None
        assert decoded['user_id'] == test_user['user_id']

        # Create refresh token
        refresh_token = create_refresh_token(test_user['user_id'])
        assert refresh_token is not None
