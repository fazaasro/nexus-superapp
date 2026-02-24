"""
Main FastAPI application
"""
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from core.database import init_db, get_user_from_email
from core.auth import (
    get_current_user_cloudflare,
    UserLogin,
    UserRegister,
    Token,
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token
)

# Import module routers
from modules.bag.api import router as bag_router
from modules.brain.api import router as brain_router
from modules.circle.api import router as circle_router
from modules.vessel.api import router as vessel_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    # Startup
    init_db()
    print("🚀 Levy API starting up...")
    print("   - Database initialized")
    print("   - Modules loaded: bag, brain, circle, vessel")
    yield
    # Shutdown
    print("👋 Levy API shutting down...")

app = FastAPI(
    title="Levy API",
    description="AAC System API - The Bag, The Brain, The Circle, The Vessel",
    version="1.0.0",
    lifespan=lifespan
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Authentication dependency - use auth module implementation
get_current_user = get_current_user_cloudflare

# Health check
@app.get("/health")
async def health_check():
    return {
        "status": "ok",
        "service": "levy-api",
        "version": "1.0.0",
        "modules": ["bag", "brain", "circle", "vessel"]
    }


# ==================== AUTHENTICATION ENDPOINTS ====================

@app.post("/api/v1/auth/login", response_model=Token)
async def login(credentials: UserLogin):
    """
    Login with email and password.

    Returns JWT access and refresh tokens.
    """
    from core.database import get_db

    with get_db() as conn:
        user = conn.execute(
            "SELECT id, email, password_hash, name, is_active FROM users WHERE email = ?",
            (credentials.email,)
        ).fetchone()

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    user_dict = dict(user)

    # Check if account is active
    if not user_dict.get("is_active", True):
        raise HTTPException(status_code=403, detail="Account is disabled")

    # Verify password
    password_hash = user_dict.get("password_hash")
    if not password_hash or not verify_password(credentials.password, password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Update last login
    from core.database import now_iso
    with get_db() as conn:
        conn.execute(
            "UPDATE users SET last_login = ? WHERE id = ?",
            (now_iso(), user_dict["id"])
        )

    # Generate tokens
    access_token = create_access_token(user_dict["id"], user_dict["email"])
    refresh_token = create_refresh_token(user_dict["id"], user_dict["email"])

    return Token(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        expires_in=60 * 60 * 24 * 7  # 7 days
    )


@app.post("/api/v1/auth/register", response_model=Token)
async def register(user_data: UserRegister):
    """
    Register a new user.

    Returns JWT access and refresh tokens.
    """
    from core.database import get_db, generate_uuid, now_iso

    # Check if email already exists
    with get_db() as conn:
        existing = conn.execute(
            "SELECT id FROM users WHERE email = ?",
            (user_data.email,)
        ).fetchone()

        if existing:
            raise HTTPException(status_code=400, detail="Email already registered")

        # Generate user ID from email (first part before @)
        user_id = user_data.email.split("@")[0].lower()

        # Check if user_id already exists
        existing_id = conn.execute(
            "SELECT id FROM users WHERE id = ?",
            (user_id,)
        ).fetchone()

        if existing_id:
            raise HTTPException(
                status_code=400,
                detail="Username already taken"
            )

        # Hash password
        password_hash = hash_password(user_data.password)

        # Insert new user
        conn.execute(
            """INSERT INTO users (id, email, name, timezone, password_hash, is_active, email_verified)
               VALUES (?, ?, ?, ?, ?, 1, 0)""",
            (user_id, user_data.email, user_data.name, user_data.timezone, password_hash)
        )

    # Generate tokens
    access_token = create_access_token(user_id, user_data.email)
    refresh_token = create_refresh_token(user_id, user_data.email)

    return Token(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        expires_in=60 * 60 * 24 * 7  # 7 days
    )


@app.post("/api/v1/auth/refresh")
async def refresh_token(refresh_token: str):
    """
    Refresh an access token using a refresh token.
    """
    from core.auth import verify_token

    try:
        token_data = verify_token(refresh_token)

        # Generate new access token
        new_access_token = create_access_token(token_data.user_id, token_data.email)

        return {
            "access_token": new_access_token,
            "token_type": "bearer"
        }
    except HTTPException:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Token refresh failed")


@app.get("/api/v1/auth/me")
async def get_current_user_info(user: dict = Depends(get_current_user)):
    """
    Get current authenticated user information.
    """
    from core.database import get_db

    with get_db() as conn:
        user_data = conn.execute(
            """SELECT id, email, name, timezone, last_login, is_active, email_verified
               FROM users WHERE id = ?""",
            (user["user_id"],)
        ).fetchone()

    if not user_data:
        raise HTTPException(status_code=404, detail="User not found")

    return dict(user_data)


@app.post("/api/v1/auth/logout")
async def logout(user: dict = Depends(get_current_user)):
    """
    Logout current user.

    Note: In a JWT-based system, logout is client-side (token deletion).
    For token revocation, implement a blacklist.
    """
    return {"message": "Logged out successfully"}

# Module routers
app.include_router(bag_router, prefix="/api/v1/bag", tags=["The Bag"])
app.include_router(brain_router, prefix="/api/v1/brain", tags=["The Brain"])
app.include_router(circle_router, prefix="/api/v1/circle", tags=["The Circle"])
app.include_router(vessel_router, prefix="/api/v1/vessel", tags=["The Vessel"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
