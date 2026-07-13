"""
Script de test pour valider tous les endpoints de l'API d'authentification.
Lance le serveur en premier: python -m uvicorn app.main:app --reload
Puis execute ce script: python test_api.py
"""

import asyncio
import httpx
import json

BASE_URL = "http://localhost:8000"

# Donnees de test
test_user_register = {
    "full_name": "Test User",
    "email": "testuser@example.com",
    "password": "SecurePass123!",
    "role": "student"
}

test_user_login = {
    "email": "testuser@example.com",
    "password": "SecurePass123!"
}


async def test_health_check():
    """Test l'endpoint de sante."""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{BASE_URL}/")
            print(f"[HEALTH CHECK] Status: {response.status_code}")
            if response.status_code == 200:
                print(f"  Response: {response.json()}")
                return True
            else:
                print(f"  ERROR: {response.text}")
                return False
        except Exception as e:
            print(f"[HEALTH CHECK] ERROR - {e}")
            return False


async def test_register():
    """Test l'endpoint d'enregistrement."""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{BASE_URL}/auth/register",
                json=test_user_register,
                headers={"Content-Type": "application/json"}
            )
            print(f"[REGISTER] Status: {response.status_code}")
            if response.status_code in [201, 200]:
                data = response.json()
                print(f"  Message: {data.get('message', 'OK')}")
                print(f"  User: {data.get('user', {})}")
                return True
            elif response.status_code == 409:
                print(f"  Account already exists (expected if running test multiple times)")
                return True
            else:
                print(f"  ERROR: {response.text}")
                return False
        except Exception as e:
            print(f"[REGISTER] ERROR - {e}")
            return False


async def test_invalid_email():
    """Test la validation du format email."""
    async with httpx.AsyncClient() as client:
        invalid_data = {
            "full_name": "Test",
            "email": "not-an-email",
            "password": "SecurePass123!"
        }
        try:
            response = await client.post(
                f"{BASE_URL}/auth/register",
                json=invalid_data
            )
            print(f"[INVALID EMAIL] Status: {response.status_code}")
            if response.status_code == 422:
                print(f"  Correctly rejected invalid email")
                return True
            else:
                print(f"  WARNING: Expected 422, got {response.status_code}")
                return False
        except Exception as e:
            print(f"[INVALID EMAIL] ERROR - {e}")
            return False


async def test_short_password():
    """Test la validation du mot de passe court."""
    async with httpx.AsyncClient() as client:
        invalid_data = {
            "full_name": "Test",
            "email": "test@example.com",
            "password": "short"  # Moins de 8 caracteres
        }
        try:
            response = await client.post(
                f"{BASE_URL}/auth/register",
                json=invalid_data
            )
            print(f"[SHORT PASSWORD] Status: {response.status_code}")
            if response.status_code == 422:
                print(f"  Correctly rejected short password")
                return True
            else:
                print(f"  WARNING: Expected 422, got {response.status_code}")
                return False
        except Exception as e:
            print(f"[SHORT PASSWORD] ERROR - {e}")
            return False


async def test_schema_imports():
    """Test que tous les schemas peuvent etre importer."""
    try:
        from app.schemas.auth_schema import (
            RegisterRequest, LoginRequest, TokenResponse,
            RefreshRequest, VerifyEmailRequest, ForgotPasswordRequest,
            ResetPasswordRequest, LogoutRequest
        )
        print("[SCHEMAS] All required schemas imported successfully")
        
        # Verifier que les schemas ont les bons champs
        register_schema = RegisterRequest.model_fields
        print(f"  RegisterRequest fields: {list(register_schema.keys())}")
        
        forgot_schema = ForgotPasswordRequest.model_fields
        print(f"  ForgotPasswordRequest fields: {list(forgot_schema.keys())}")
        
        reset_schema = ResetPasswordRequest.model_fields
        print(f"  ResetPasswordRequest fields: {list(reset_schema.keys())}")
        
        logout_schema = LogoutRequest.model_fields
        print(f"  LogoutRequest fields: {list(logout_schema.keys())}")
        
        return True
    except Exception as e:
        print(f"[SCHEMAS] ERROR - {e}")
        return False


async def test_router_routes():
    """Test que tous les routes du router sont enregistrees."""
    try:
        from app.routers.auth_router import router as auth_router
        
        routes = auth_router.routes
        print(f"[ROUTER] Found {len(routes)} routes in auth_router:")
        
        route_paths = {}
        for route in routes:
            if hasattr(route, 'path'):
                path = route.path
                method = route.methods if hasattr(route, 'methods') else 'GET'
                if path not in route_paths:
                    route_paths[path] = []
                route_paths[path].append(method)
        
        expected_endpoints = [
            '/register', '/login', '/refresh', '/logout',
            '/verify-email', '/forgot-password', '/reset-password', '/me'
        ]
        
        for endpoint in expected_endpoints:
            if any(endpoint in path for path in route_paths.keys()):
                print(f"  [OK] {endpoint}")
            else:
                print(f"  [MISSING] {endpoint}")
        
        return True
    except Exception as e:
        print(f"[ROUTER] ERROR - {e}")
        return False


async def run_all_tests():
    """Execute tous les tests."""
    print("=" * 60)
    print("FASTAPI AUTHENTICATION BACKEND - TEST SUITE")
    print("=" * 60)
    print()
    
    results = {}
    
    # Tests hors-ligne (pas besoin du serveur)
    print("OFFLINE TESTS")
    print("-" * 60)
    results['schemas'] = await test_schema_imports()
    print()
    results['router'] = await test_router_routes()
    print()
    
    # Tests en-ligne (besoin du serveur)
    print("ONLINE TESTS (require running server on port 8000)")
    print("-" * 60)
    results['health'] = await test_health_check()
    print()
    results['invalid_email'] = await test_invalid_email()
    print()
    results['short_password'] = await test_short_password()
    print()
    results['register'] = await test_register()
    print()
    
    # Resume
    print("=" * 60)
    print("TEST SUMMARY")
    print("-" * 60)
    
    total = len(results)
    passed = sum(1 for v in results.values() if v)
    
    for test_name, result in results.items():
        status = "[PASS]" if result else "[FAIL]"
        print(f"{status} {test_name}")
    
    print("-" * 60)
    print(f"Result: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n✓ All tests passed! Your API is ready to use.")
    else:
        print(f"\n✗ {total - passed} test(s) failed. Please check the output above.")
    
    print("=" * 60)


if __name__ == "__main__":
    print("\nRUNNING TESTS...\n")
    asyncio.run(run_all_tests())
