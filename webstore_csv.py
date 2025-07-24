"""
WebStore with CSV Repository - Example using CSV storage
"""
import sys
from pathlib import Path

# Add src to path
from src.repositories.csv_repository import CSVRepository
from src.services.product_service import ProductService
from src.services.user_service import UserService
from src.services.cart_service import CartService
from src.controllers.product_controller import ProductController
from src.controllers.user_controller import UserController
from src.controllers.cart_controller import CartController
from src.views.cli_interface import WebStoreInterface

sys.path.append(str(Path(__file__).parent / "src"))


def main():
    """Main application with CSV storage"""
    # Initialize CSV repository
    repository = CSVRepository("data_csv")
    
    # Initialize services with CSV repository
    product_service = ProductService(repository)
    user_service = UserService(repository)
    cart_service = CartService(product_service)
    
    # Initialize controllers
    product_controller = ProductController(product_service)
    user_controller = UserController(user_service)
    cart_controller = CartController(cart_service, user_controller)
    
    # Initialize CLI interface
    interface = WebStoreInterface(
        product_controller,
        user_controller,
        cart_controller
    )
    
    # Add some sample data if CSV files are empty
    if not repository.load_all('products'):
        print("Adding sample products to CSV...")
        sample_products = [
            {
                'id': 'p1',
                'name': 'Laptop Pro',
                'price': 999.99,
                'category': 'Electronics',
                'stock': 10,
                'description': 'High-performance laptop'
            },
            {
                'id': 'p2',
                'name': 'Coffee Mug',
                'price': 12.99,
                'category': 'Kitchen',
                'stock': 25,
                'description': 'Ceramic coffee mug'
            }
        ]
        
        for product in sample_products:
            repository.save('products', product)
    
    # Add sample admin user
    if not repository.load_all('users'):
        print("Adding sample admin user to CSV...")
        repository.save('users', {
            'id': 'u1',
            'username': 'admin',
            'email': 'admin@webstore.com',
            'role': 'admin',
            'created_at': '2025-01-01'
        })
    
    print("🛍️ WebStore with CSV Storage Starting...")
    print("Data stored in: data_csv/ directory")
    print("-" * 40)
    
    # Run the application
    interface.run()


if __name__ == "__main__":
    main()
