"""
Authentication module for Nexus Super App
Provides JWT token generation/validation, password hashing, and OAuth support
"""
import logging
import os
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List
from dotenv import load_dotenv
import bcrypt
import jwt
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-this-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days
REFRESH_TOKEN_EXPIRE_DAYS = 30

# OAuth Configuration (Google)
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI")

# HTTP Bearer token scheme
security = HTTPBearer()


# ==================== MODELS ====================

class Token(BaseModel):
    """JWT Token response model"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int


class TokenData(BaseModel):
    """Token payload data model"""
    user_id: str
    email: str
    exp: Optional[int] = None


class UserLogin(BaseModel):
    """User login request model"""
    email: str
    password: str


class UserRegister(BaseModel):
    """User registration request model"""
    email: str
    password: str
    name: str
    timezone: str = "Europe/Berlin"


class OAuthCallback(BaseModel):
    """OAuth callback request model"""
    code: str
    state: Optional[str] = None


# ==================== PASSWORD HASHING ====================

def hash_password(password: str) -> str:
    """
    Hash a password using bcrypt.

    Args:
        password: Plain text password

    Returns:
        Hashed password string

    Example:
        >>> hashed = hash_password("mypassword")
        >>> print(hashed)  # $2b$12$...
    """
    try:
        # Convert password to bytes
        password_bytes = password.encode('utf-8')
        # Generate salt and hash password
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password_bytes, salt)
        # Return as string
        return hashed.decode('utf-8')
    except Exception as e:
        logger.error(f"Password hashing failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to hash password"
        )


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against its hash.

    Args:
        plain_password: Plain text password to verify
        hashed_password: Hashed password to compare against

    Returns:
        True if password matches, False otherwise

    Example:
        >>> if verify_password("mypassword", hashed):
        ...     print("Password correct")
    """
    try:
        # Convert to bytes
        plain_bytes = plain_password.encode('utf-8')
        hashed_bytes = hashed_password.encode('utf-8')
        # Verify
        return bcrypt.checkpw(plain_bytes, hashed_bytes)
    except Exception as e:
        logger.error(f"Password verification failed: {e}")
        return False


# ==================== JWT TOKENS ====================

def create_access_token(
    user_id: str,
    email: str,
    expires_delta: Optional[timedelta] = None
) -> str:
    """
    Create a JWT access token.

    Args:
        user_id: User's unique identifier
        email: User's email address
        expires_delta: Optional custom expiration time

    Returns:
        Encoded JWT token string

    Example:
        >>> token = create_access_token("faza", "faza@example.com")
        >>> print(token)  # eyJhbGciOiJIUzI1NiIs...
    """
    try:
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

        to_encode = {
            "sub": user_id,
            "email": email,
            "exp": expire,
            "iat": datetime.utcnow(),
            "type": "access"
        }

        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        logger.info(f"Access token created for user {user_id}")
        return encoded_jwt
    except Exception as e:
        logger.error(f"Failed to create access token: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create access token"
        )


def create_refresh_token(user_id: str, email: str) -> str:
    """
    Create a JWT refresh token (longer expiration).

    Args:
        user_id: User's unique identifier
        email: User's email address

    Returns:
        Encoded JWT refresh token string

    Example:
        >>> token = create_refresh_token("faza", "faza@example.com")
    """
    try:
        expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)

        to_encode = {
            "sub": user_id,
            "email": email,
            "exp": expire,
            "iat": datetime.utcnow(),
            "type": "refresh"
        }

        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        logger.info(f"Refresh token created for user {user_id}")
        return encoded_jwt
    except Exception as e:
        logger.error(f"Failed to create refresh token: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create refresh token"
        )


def verify_token(token: str) -> TokenData:
    """
    Verify and decode a JWT token.

    Args:
        token: JWT token string

    Returns:
        TokenData object with user information

    Raises:
        HTTPException: If token is invalid or expired

    Example:
        >>> data = verify_token(token)
        >>> print(data.user_id)  # "faza"
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        email: str = payload.get("email")
        exp: int = payload.get("exp")

        if user_id is None or email is None:
            logger.warning("Token missing required fields")
            raise credentials_exception

        # Check expiration
        if datetime.utcnow() > datetime.fromtimestamp(exp):
            logger.warning("Token expired")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired"
            )

        token_data = TokenData(user_id=user_id, email=email, exp=exp)
        logger.debug(f"Token verified for user {user_id}")
        return token_data

    except JWTError as e:
        logger.error(f"JWT validation failed: {e}")
        raise credentials_exception
    except Exception as e:
        logger.error(f"Unexpected error verifying token: {e}")
        raise credentials_exception


# ==================== AUTHENTICATION DEPENDENCIES ====================

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> Dict[str, Any]:
    """
    FastAPI dependency to extract and verify user from JWT token.

    Args:
        credentials: HTTP Bearer credentials

    Returns:
        Dictionary with user information

    Raises:
        HTTPException: If authentication fails

    Example:
        @router.get("/protected")
        async def protected_route(user: dict = Depends(get_current_user)):
            return {"message": f"Hello {user['email']}"}
    """
    try:
        token = credentials.credentials
        token_data = verify_token(token)

        return {
            "user_id": token_data.user_id,
            "email": token_data.email
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Authentication failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication failed"
        )


async def get_current_user_optional(
    request: Request
) -> Optional[Dict[str, Any]]:
    """
    Optional authentication - returns None if not authenticated.

    Args:
        request: FastAPI Request object

    Returns:
        Dictionary with user info or None

    Example:
        @router.get("/optional")
        async def optional_route(user: Optional[dict] = Depends(get_current_user_optional)):
            if user:
                return {"message": f"Hello {user['email']}"}
            return {"message": "Hello anonymous"}
    """
    try:
        # Try to get token from Authorization header
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return None

        token = auth_header.split(" ")[1]
        token_data = verify_token(token)

        return {
            "user_id": token_data.user_id,
            "email": token_data.email
        }
    except HTTPException:
        return None
    except Exception as e:
        logger.debug(f"Optional auth failed: {e}")
        return None


# ==================== OAUTH SUPPORT ====================

async def get_google_oauth_url() -> str:
    """
    Generate Google OAuth 2.0 authorization URL.

    Returns:
        OAuth authorization URL

    Example:
        >>> url = await get_google_oauth_url()
        >>> print(url)  # https://accounts.google.com/o/oauth2/v2/auth?...
    """
    try:
        if not all([GOOGLE_CLIENT_ID, GOOGLE_REDIRECT_URI]):
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Google OAuth not configured"
            )

        from authlib.integrations.starlette_client import OAuth

        oauth = OAuth()
        oauth.register(
            name='google',
            client_id=GOOGLE_CLIENT_ID,
            client_secret=GOOGLE_CLIENT_SECRET,
            server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
            client_kwargs={'scope': 'openid email profile'}
        )

        return oauth.google.authorize_redirect(GOOGLE_REDIRECT_URI)

    except Exception as e:
        logger.error(f"Failed to generate Google OAuth URL: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate OAuth URL"
        )


async def handle_google_oauth_callback(code: str) -> Dict[str, Any]:
    """
    Handle Google OAuth callback and return user info.

    Args:
        code: OAuth authorization code

    Returns:
        Dictionary with user information and tokens

    Example:
        >>> result = await handle_google_oauth_callback("auth_code")
        >>> print(result['user_id'])
    """
    try:
        if not all([GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, GOOGLE_REDIRECT_URI]):
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Google OAuth not configured"
            )

        from authlib.integrations.starlette_client import OAuth
        import httpx

        # Exchange code for tokens
        async with httpx.AsyncClient() as client:
            token_response = await client.post(
                "https://oauth2.googleapis.com/token",
                data={
                    "code": code,
                    "client_id": GOOGLE_CLIENT_ID,
                    "client_secret": GOOGLE_CLIENT_SECRET,
                    "redirect_uri": GOOGLE_REDIRECT_URI,
                    "grant_type": "authorization_code"
                }
            )
            token_response.raise_for_status()
            tokens = token_response.json()

        # Get user info
        async with httpx.AsyncClient() as client:
            user_response = await client.get(
                "https://www.googleapis.com/oauth2/v2/userinfo",
                headers={"Authorization": f"Bearer {tokens['access_token']}"}
            )
            user_response.raise_for_status()
            user_info = user_response.json()

        email = user_info.get("email")
        name = user_info.get("name", "")

        if not email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Could not retrieve email from OAuth provider"
            )

        # Map email to user_id (existing logic)
        from core.database import get_user_from_email
        user_id = get_user_from_email(email)

        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User not authorized"
            )

        # Create JWT tokens
        access_token = create_access_token(user_id, email)
        refresh_token = create_refresh_token(user_id, email)

        logger.info(f"Google OAuth successful for user {user_id}")

        return {
            "user_id": user_id,
            "email": email,
            "name": name,
            "access_token": access_token,
            "refresh_token": refresh_token
        }

    except httpx.HTTPStatusError as e:
        logger.error(f"Google OAuth HTTP error: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="OAuth token exchange failed"
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Google OAuth callback failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="OAuth callback failed"
        )


# ==================== CLOUDFLARE ACCESS INTEGRATION ====================

async def get_current_user_cloudflare(request: Request) -> Dict[str, Any]:
    """
    Extract user from Cloudflare Access headers.
    Falls back to JWT token for flexibility.

    Args:
        request: FastAPI Request object

    Returns:
        Dictionary with user information

    Raises:
        HTTPException: If authentication fails

    Example:
        @router.get("/protected")
        async def protected_route(user: dict = Depends(get_current_user_cloudflare)):
            return {"message": f"Hello {user['email']}"}
    """
    from core.database import get_user_from_email

    # Try Cloudflare Access headers first
    email = request.headers.get("CF-Access-Authenticated-User-Email")
    if email:
        user_id = get_user_from_email(email)
        if user_id:
            logger.debug(f"User authenticated via Cloudflare Access: {email}")
            return {
                "user_id": user_id,
                "email": email
            }

    # Fallback to test header for development
    email = request.headers.get("X-Test-User")
    if email:
        user_id = get_user_from_email(email)
        if user_id:
            logger.debug(f"User authenticated via test header: {email}")
            return {
                "user_id": user_id,
                "email": email
            }

    # Try JWT token as fallback
    try:
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
            token_data = verify_token(token)
            logger.debug(f"User authenticated via JWT: {token_data.email}")
            return {
                "user_id": token_data.user_id,
                "email": token_data.email
            }
    except Exception:
        pass

    # No valid authentication found
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Not authenticated"
    )


# ==================== UTILITY FUNCTIONS ====================

def is_token_expired(token: str) -> bool:
    """
    Check if a token is expired without throwing an exception.

    Args:
        token: JWT token string

    Returns:
        True if token is expired, False otherwise
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM], options={"verify_exp": True})
        exp = payload.get("exp")
        if exp:
            return datetime.utcnow() > datetime.fromtimestamp(exp)
        return True
    except JWTError:
        return True
    except Exception as e:
        logger.error(f"Error checking token expiration: {e}")
        return True


def extract_user_id_from_token(token: str) -> Optional[str]:
    """
    Extract user_id from token without validation (use carefully).

    Args:
        token: JWT token string

    Returns:
        User ID or None if extraction fails
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM], options={"verify_signature": False})
        return payload.get("sub")
    except Exception as e:
        logger.error(f"Failed to extract user_id from token: {e}")
        return None
