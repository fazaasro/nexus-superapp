"""
Main FastAPI application
"""
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from core.database import init_db, get_user_from_email

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

# Authentication dependency
async def get_current_user(request: Request):
    """Extract user from Cloudflare Access headers"""
    # For testing without Cloudflare
    email = request.headers.get("CF-Access-Authenticated-User-Email")
    
    # Fallback for testing
    if not email:
        # Check for test header
        email = request.headers.get("X-Test-User")
    
    if not email:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    user_id = get_user_from_email(email)
    if not user_id:
        raise HTTPException(status_code=403, detail="User not authorized")
    
    return {
        "email": email,
        "user_id": user_id
    }

# Health check
@app.get("/health")
async def health_check():
    return {
        "status": "ok",
        "service": "levy-api",
        "version": "1.0.0",
        "modules": ["bag", "brain", "circle", "vessel"]
    }

# Module routers
app.include_router(bag_router, prefix="/api/v1/bag", tags=["The Bag"])
app.include_router(brain_router, prefix="/api/v1/brain", tags=["The Brain"])
app.include_router(circle_router, prefix="/api/v1/circle", tags=["The Circle"])
app.include_router(vessel_router, prefix="/api/v1/vessel", tags=["The Vessel"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
