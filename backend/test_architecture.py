#!/usr/bin/env python3
"""
Test script untuk verifikasi Clean Architecture
"""
import sys
import time
import json

def test_imports():
    """Test semua imports"""
    print("=" * 60)
    print("TEST 1: Imports")
    print("=" * 60)
    
    try:
        from config.settings import settings
        print("✓ Config settings imported")
        print(f"  App: {settings.APP_NAME}")
        print(f"  Version: {settings.APP_VERSION}")
    except Exception as e:
        print(f"✗ Config import failed: {e}")
        return False
    
    try:
        from config.database import get_db_connection, get_db_cursor
        print("✓ Database config imported")
    except Exception as e:
        print(f"✗ Database config import failed: {e}")
        return False
    
    try:
        from repositories.lokasi_repository import LokasiRepository
        print("✓ Lokasi repository imported")
    except Exception as e:
        print(f"✗ Repository import failed: {e}")
        return False
    
    try:
        from services.lokasi_service import LokasiService
        print("✓ Lokasi service imported")
    except Exception as e:
        print(f"✗ Service import failed: {e}")
        return False
    
    try:
        from api.v1.schemas import LokasiCreate, LokasiResponse
        print("✓ API schemas imported")
    except Exception as e:
        print(f"✗ Schemas import failed: {e}")
        return False
    
    try:
        from main import app
        print("✓ FastAPI app imported")
        routes = [r.path for r in app.routes if hasattr(r, 'path')]
        api_routes = [r for r in routes if '/api/v1/' in r]
        print(f"  Total routes: {len(routes)}")
        print(f"  API v1 routes: {len(api_routes)}")
    except Exception as e:
        print(f"✗ App import failed: {e}")
        return False
    
    print("\n✓ All imports successful!\n")
    return True


def test_architecture():
    """Test clean architecture structure"""
    print("=" * 60)
    print("TEST 2: Clean Architecture Structure")
    print("=" * 60)
    
    import os
    from pathlib import Path
    
    backend_dir = Path(__file__).parent
    
    # Check directories
    dirs_to_check = [
        'api/v1/endpoints',
        'services',
        'repositories',
        'config',
        'utils'
    ]
    
    for dir_path in dirs_to_check:
        full_path = backend_dir / dir_path
        if full_path.exists():
            print(f"✓ {dir_path}/ exists")
        else:
            print(f"✗ {dir_path}/ missing")
            return False
    
    # Check key files
    files_to_check = [
        'main.py',
        'config/settings.py',
        'config/database.py',
        'repositories/lokasi_repository.py',
        'services/lokasi_service.py',
        'api/v1/endpoints/lokasi.py',
        'api/v1/router.py',
        'api/v1/schemas.py',
    ]
    
    for file_path in files_to_check:
        full_path = backend_dir / file_path
        if full_path.exists():
            print(f"✓ {file_path} exists")
        else:
            print(f"✗ {file_path} missing")
            return False
    
    print("\n✓ Clean architecture structure verified!\n")
    return True


def main():
    """Run all tests"""
    print("\n🧪 Testing Clean Architecture Implementation\n")
    
    # Change to backend directory
    import os
    backend_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(backend_dir)
    
    # Run tests
    test_results = []
    
    test_results.append(("Imports", test_imports()))
    test_results.append(("Architecture", test_architecture()))
    
    # Summary
    print("=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    all_passed = True
    for test_name, result in test_results:
        status = "✓ PASSED" if result else "✗ FAILED"
        print(f"{test_name}: {status}")
        if not result:
            all_passed = False
    
    print("=" * 60)
    
    if all_passed:
        print("\n🎉 All tests passed! Clean Architecture implemented successfully!\n")
        print("To start the server:")
        print("  cd /home/sultan/fast/fast-attendance/backend")
        print("  uvicorn main:app --reload --host 0.0.0.0 --port 8000")
        print("\nThen visit: http://localhost:8000/docs")
        return 0
    else:
        print("\n❌ Some tests failed. Please check the errors above.\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())
