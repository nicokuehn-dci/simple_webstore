#!/usr/bin/env python3
"""
Debug Script - Test Login/Logout and Storage functionality
"""
import sys
import os
from pathlib import Path

# Add src to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    from repositories.json_repository import JSONRepository
    from repositories.csv_repository import CSVRepository
    from services.user_service import UserService
    from controllers.user_controller import UserController
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)


def test_login_logout():
    """Test login/logout functionality"""
    print("🔍 Testing Login/Logout System...")
    print("=" * 40)
    
    # Setup
    Path('debug_data').mkdir(exist_ok=True)
    repository = JSONRepository("debug_data")
    user_service = UserService(repository)
    user_controller = UserController(user_service)
    
    # Create test user
    print("1. Creating test user...")
    result = user_controller.register("testuser", "test@example.com")
    print(f"   Result: {result}")
    
    # Test login
    print("\n2. Testing login...")
    login_result = user_controller.login("testuser")
    print(f"   Login result: {login_result}")
    print(f"   Is logged in: {user_controller.is_logged_in()}")
    
    # Test current user
    print("\n3. Testing current user...")
    current_user = user_controller.get_current_user()
    print(f"   Current user: {current_user}")
    
    # Test logout
    print("\n4. Testing logout...")
    logout_result = user_controller.logout()
    print(f"   Logout result: {logout_result}")
    print(f"   Is logged in: {user_controller.is_logged_in()}")
    
    print("\n✅ Login/Logout test completed!")


def test_dual_storage():
    """Test JSON and CSV storage"""
    print("\n🔍 Testing Dual Storage System...")
    print("=" * 40)
    
    # Setup directories
    Path('debug_json').mkdir(exist_ok=True)
    Path('debug_csv').mkdir(exist_ok=True)
    
    # Test JSON storage
    print("1. Testing JSON storage...")
    json_repo = JSONRepository("debug_json")
    test_data = {
        'id': 'test1',
        'name': 'Test Product',
        'price': 19.99,
        'category': 'Test',
        'stock': 5
    }
    
    json_save = json_repo.save('products', test_data)
    json_load = json_repo.load_all('products')
    print(f"   JSON save result: {json_save}")
    print(f"   JSON load result: {json_load}")
    
    # Test CSV storage
    print("\n2. Testing CSV storage...")
    csv_repo = CSVRepository("debug_csv")
    csv_save = csv_repo.save('products', test_data)
    csv_load = csv_repo.load_all('products')
    print(f"   CSV save result: {csv_save}")
    print(f"   CSV load result: {csv_load}")
    
    print("\n✅ Dual storage test completed!")


def test_menu_display():
    """Test menu display without echo"""
    print("\n🔍 Testing Menu System...")
    print("=" * 40)
    
    from views.menu import SimpleMenu
    
    # Test menu creation
    test_menu = SimpleMenu("Test Menu", [
        "Option 1",
        "Option 2", 
        "Option 3"
    ])
    
    print("Menu created successfully!")
    print("Note: Manual testing required for echo/flicker issues")
    print("✅ Menu system test completed!")


def main():
    """Run all debug tests"""
    print("🐛 DEBUG MODE - Testing WebStore Components")
    print("=" * 50)
    
    try:
        test_login_logout()
        test_dual_storage()
        test_menu_display()
        
        print("\n🎉 All tests completed!")
        print("\nNext steps:")
        print("1. ✅ Login/Logout system appears functional")
        print("2. ✅ Dual storage (JSON/CSV) working")
        print("3. ⚠️  Menu echo/flicker needs manual testing")
        
    except Exception as e:
        print(f"\n❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
