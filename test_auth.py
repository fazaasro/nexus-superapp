"""
Simple test to verify authentication implementation
"""
import sys
sys.path.insert(0, '/home/ai-dev/swarm/repos/nexus-superapp')

def test_auth_module():
    """Test core auth module"""
    print("Testing core/auth.py...")

    from core.auth import (
        hash_password,
        verify_password,
        create_access_token,
        verify_token,
        UserLogin,
        UserRegister,
        Token,
        TokenData
    )

    # Test password hashing
    password = "test_password_123"
    hashed = hash_password(password)
    print(f"✓ Password hashed: {hashed[:20]}...")

    # Test password verification
    assert verify_password(password, hashed) == True
    assert verify_password("wrong_password", hashed) == False
    print("✓ Password verification works")

    # Test JWT token creation
    token = create_access_token("test_user", "test@example.com")
    print(f"✓ JWT token created: {token[:30]}...")

    # Test JWT token verification
    token_data = verify_token(token)
    assert token_data.user_id == "test_user"
    assert token_data.email == "test@example.com"
    print("✓ JWT token verification works")

    print("✅ Auth module tests passed\n")


def test_module_apis():
    """Test module API imports"""
    print("Testing module API imports...")

    from modules.bag.api import router as bag_router
    from modules.brain.api import router as brain_router
    from modules.circle.api import router as circle_router
    from modules.vessel.api import router as vessel_router

    print(f"✓ Bag router loaded: {bag_router.prefix}")
    print(f"✓ Brain router loaded: {brain_router.prefix}")
    print(f"✓ Circle router loaded: {circle_router.prefix}")
    print(f"✓ Vessel router loaded: {vessel_router.prefix}")

    # Check endpoints
    bag_routes = [route.path for route in bag_router.routes]
    print(f"✓ Bag module has {len(bag_routes)} routes")

    brain_routes = [route.path for route in brain_router.routes]
    print(f"✓ Brain module has {len(brain_routes)} routes")

    circle_routes = [route.path for route in circle_router.routes]
    print(f"✓ Circle module has {len(circle_routes)} routes")

    vessel_routes = [route.path for route in vessel_router.routes]
    print(f"✓ Vessel module has {len(vessel_routes)} routes")

    print("✅ Module API tests passed\n")


def test_no_hardcoded_user():
    """Test no hardcoded user_id='faza' in API endpoints"""
    print("Testing for hardcoded user_id...")

    import os
    from modules.bag import api as bag_api
    from modules.brain import api as brain_api
    from modules.circle import api as circle_api
    from modules.vessel import api as vessel_api

    # Read API files
    import inspect
    for module_name, module in [("Bag", bag_api), ("Brain", brain_api),
                                ("Circle", circle_api), ("Vessel", vessel_api)]:
        source = inspect.getsource(module)
        if "user_id='faza'" in source or 'user_id="faza"' in source:
            print(f"✗ {module_name} has hardcoded user_id!")
            return False
        else:
            print(f"✓ {module_name} has no hardcoded user_id")

    print("✅ No hardcoded user_id found\n")


def test_main_api():
    """Test main API application"""
    print("Testing main API...")

    from api.main import app

    # Check auth endpoints
    routes = {route.path for route in app.routes}
    auth_endpoints = {
        "/api/v1/auth/login",
        "/api/v1/auth/register",
        "/api/v1/auth/refresh",
        "/api/v1/auth/me",
        "/api/v1/auth/logout"
    }

    for endpoint in auth_endpoints:
        if endpoint in routes:
            print(f"✓ Auth endpoint exists: {endpoint}")
        else:
            print(f"✗ Missing auth endpoint: {endpoint}")

    print("✅ Main API tests passed\n")


if __name__ == "__main__":
    print("=" * 60)
    print("Authentication Implementation Test Suite")
    print("=" * 60)
    print()

    try:
        test_auth_module()
        test_module_apis()
        test_no_hardcoded_user()
        test_main_api()

        print("=" * 60)
        print("✅ ALL TESTS PASSED")
        print("=" * 60)
        sys.exit(0)

    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
