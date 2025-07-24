#!/usr/bin/env python3
"""
Simple WebStore - Main Entry Point
Uses the organized src/ folder structure
"""
import sys
import os
from pathlib import Path

# Add src to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Import required components
try:
    from repositories.json_repository import JSONRepository
    from services.product_service import ProductService
    from services.user_service import UserService
    from services.cart_service import CartService
    from controllers.product_controller import ProductController
    from controllers.user_controller import UserController
    from controllers.cart_controller import CartController
    from views.cli_interface import WebStoreInterface
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)


def setup_directories():
    """Create necessary directories"""
    Path('data').mkdir(exist_ok=True)


def create_sample_data(product_service, user_service):
    """Create sample data if none exists"""
    sample_products = [
        {
            "name": "Gaming Laptop",
            "price": 1299.99,
            "category": "Electronics",
            "stock": 5
        },
        {
            "name": "Wireless Mouse",
            "price": 49.99,
            "category": "Electronics",
            "stock": 15
        },
        {
            "name": "Coffee Mug",
            "price": 14.99,
            "category": "Home",
            "stock": 25
        },
        {
            "name": "Notebook",
            "price": 8.99,
            "category": "Office",
            "stock": 30
        }
    ]
    
    for product_data in sample_products:
        product_service.create_product(**product_data)
    
    user_service.register_user("admin", "admin@store.com", "admin")
    user_service.register_user("customer", "customer@store.com", "customer")


def main():
    """Main application entry point"""
    print("🛍️ Welcome to Simple WebStore!")
    print("=" * 40)
    
    # Setup
    setup_directories()
    
    # Initialize components
    repository = JSONRepository("data")
    product_service = ProductService(repository)
    user_service = UserService(repository)
    cart_service = CartService(product_service)
    
    product_controller = ProductController(product_service)
    user_controller = UserController(user_service)
    cart_controller = CartController(cart_service, user_controller)
    
    # Create sample data if needed
    if len(product_service.get_all_products()) == 0:
        create_sample_data(product_service, user_service)
    
    # Run the application
    app = WebStoreInterface(
        product_controller, user_controller, cart_controller
    )
    app.run()


if __name__ == "__main__":
    main()
