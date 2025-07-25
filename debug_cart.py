#!/usr/bin/env python3
import sys
import os

# Add src to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from repositories.json_repository import JSONRepository
from services.product_service import ProductService
from services.user_service import UserService
from services.cart_service import CartService
from controllers.user_controller import UserController
from controllers.cart_controller import CartController

def test_cart():
    print("🔍 Testing cart functionality...")
    
    repo = JSONRepository('test_data')
    product_service = ProductService(repo)
    user_service = UserService(repo)
    cart_service = CartService(product_service, 'test_data')
    user_controller = UserController(user_service, cart_service)
    cart_controller = CartController(cart_service, user_controller)

    # Create a product
    product = product_service.create_product('Test Product', 10.99, 'Test', 5)
    print(f'✅ Product created: {product.name if product else "Failed"}')

    # Register and login user
    user_service.register_user('testuser', 'test@test.com', 'customer')
    login_result = user_controller.login('testuser')
    print(f'✅ Login result: {login_result}')

    # Add to cart
    if product:
        print(f'🛒 Adding product {product.id} to cart...')
        add_result = cart_controller.add_item(product.id, 1)
        print(f'✅ Add to cart result: {add_result}')
        
        # Get cart
        print('🔍 Getting cart contents...')
        cart_result = cart_controller.get_cart()
        print(f'✅ Cart result: {cart_result}')
        
        # Check if items exist
        if cart_result.get('success') and cart_result.get('items'):
            print(f"✅ Cart has {len(cart_result['items'])} items")
            for item in cart_result['items']:
                print(f"   - {item}")
        else:
            print("❌ Cart is empty or failed to load")
            print(f"   Success: {cart_result.get('success')}")
            print(f"   Items: {cart_result.get('items')}")
            print(f"   Error: {cart_result.get('error')}")

if __name__ == "__main__":
    test_cart()
