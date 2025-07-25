#!/usr/bin/env python3
"""
Test cart viewing functionality directly
"""
import sys
import os

# Add src to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    from repositories.json_repository import JSONRepository
    from services.product_service import ProductService
    from services.cart_service import CartService
    from controllers.cart_viewing import CartViewing
    from controllers.user_controller import UserController
    from services.user_service import UserService
    
    print("✅ All imports successful")
    
    # Setup services
    repository = JSONRepository("test_data")
    product_service = ProductService(repository)
    user_service = UserService(repository)
    cart_service = CartService(product_service, "test_data")
    user_controller = UserController(user_service, cart_service)
    
    # Create a test product
    product_result = product_service.create_product(
        name="Test Product",
        price=10.99,
        category="Test",
        stock=10
    )
    print(f"✅ Product created: {product_result}")
    
    # Register and login test user
    user_result = user_service.register_user("testuser", "test@test.com", "customer")
    print(f"✅ User registered: {user_result}")
    
    login_result = user_controller.login("testuser")
    print(f"✅ User logged in: {login_result}")
    
    # Add item to cart
    if product_result['success']:
        product_id = product_result['product']['id']
        add_result = cart_service.add_to_cart("testuser", product_id, 2)
        print(f"✅ Added to cart: {add_result}")
        
        # Test cart viewing
        cart_viewing = CartViewing(cart_service, user_controller)
        cart_result = cart_viewing.get_cart()
        print(f"✅ Cart viewing result: {cart_result}")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
