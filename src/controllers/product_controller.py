"""
Product Controller - Main coordinator for product operations
"""
from typing import Dict
from src.services.product_service import ProductService
from .product_operations import ProductOperations
from .product_search import ProductSearch
from .product_management import ProductManagement


class ProductController:
    """Main controller that coordinates all product operations"""
    
    def __init__(self, product_service: ProductService):
        """Initialize controller with all product components"""
        self.product_service = product_service
        
        # Initialize components
        self.operations = ProductOperations(product_service)
        self.search = ProductSearch(product_service)
        self.management = ProductManagement(product_service)
    
    # Operations
    def create_product(self, name: str, price: float, category: str,
                      stock: int = 0, description: str = "") -> Dict:
        return self.operations.create_product(name, price, category, stock, description)
    
    def update_product(self, product_id: str, **kwargs) -> Dict:
        return self.operations.update_product(product_id, **kwargs)
    
    def delete_product(self, product_id: str) -> Dict:
        return self.operations.delete_product(product_id)
    
    # Search and browsing
    def list_products(self, category: str = None) -> Dict:
        return self.search.list_products(category)
    
    def get_product(self, product_id: str) -> Dict:
        return self.search.get_product(product_id)
    
    def search_products(self, query: str) -> Dict:
        return self.search.search_products(query)
    
    def get_categories(self) -> Dict:
        return self.search.get_categories()
    
    def get_products_by_category(self, category: str) -> Dict:
        return self.search.get_products_by_category(category)
    
    # Management operations
    def get_low_stock_products(self, threshold: int = 5) -> Dict:
        return self.management.get_low_stock_products(threshold)
    
    def apply_category_discount(self, category: str, discount_percent: float) -> Dict:
        return self.management.apply_category_discount(category, discount_percent)
    
    def get_product_stats(self) -> Dict:
        return self.management.get_product_stats()
    
    def bulk_update_stock(self, updates: Dict[str, int]) -> Dict:
        return self.management.bulk_update_stock(updates)
