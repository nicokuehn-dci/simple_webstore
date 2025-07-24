"""Test CSV Repository"""
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent / "src"))

from src.repositories.csv_repository import CSVRepository

def test_csv():
    repo = CSVRepository('test_csv')
    
    # Test product
    test_product = {
        'id': 'test1',
        'name': 'Test Product', 
        'price': 19.99,
        'category': 'Test',
        'stock': 5,
        'description': 'Test item'
    }
    
    print("Testing CSV Repository...")
    result = repo.save('products', test_product)
    print(f"Save result: {result}")
    
    loaded = repo.load_all('products')
    print(f"Loaded products: {loaded}")
    
    # Test user
    test_user = {
        'id': 'u1',
        'username': 'testuser',
        'email': 'test@test.com',
        'role': 'customer',
        'created_at': '2025-01-01'
    }
    
    repo.save('users', test_user)
    users = repo.load_all('users')
    print(f"Loaded users: {users}")

if __name__ == "__main__":
    test_csv()
