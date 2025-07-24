"""
Product Search - Handle product searching and browsing
"""
from typing import Dict
from src.services.product_service import ProductService


class ProductSearch:
    """Handles product search and browsing operations"""
    
    def __init__(self, product_service: ProductService):
        self.product_service = product_service
    
    def list_products(self, category: str = None) -> Dict:
        """List all products or products by category"""
        try:
            if category:
                products = self.product_service.get_products_by_category(category)
            else:
                products = self.product_service.get_all_products()
            
            return {
                'success': True,
                'products': [self._format_product(p) for p in products],
                'count': len(products)
            }
        except Exception as e:
            return {'success': False, 'error': f'Failed to load products: {e}'}
    
    def get_product(self, product_id: str) -> Dict:
        """Get single product by ID"""
        product = self.product_service.get_product_by_id(product_id)
        
        if product:
            return {
                'success': True,
                'product': self._format_product(product)
            }
        else:
            return {'success': False, 'error': 'Product not found'}
    
    def search_products(self, query: str) -> Dict:
        """Search products by name or description"""
        if not query.strip():
            return {'success': False, 'error': 'Search query is required'}
        
        try:
            products = self.product_service.search_products(query)
            return {
                'success': True,
                'products': [self._format_product(p) for p in products],
                'count': len(products),
                'query': query
            }
        except Exception as e:
            return {'success': False, 'error': f'Search failed: {e}'}
    
    def get_categories(self) -> Dict:
        """Get all product categories"""
        try:
            categories = self.product_service.get_categories()
            return {
                'success': True,
                'categories': categories,
                'count': len(categories)
            }
        except Exception as e:
            return {'success': False, 'error': f'Failed to load categories: {e}'}
    
    def get_products_by_category(self, category: str) -> Dict:
        """Get products by specific category"""
        try:
            products = self.product_service.get_products_by_category(category)
            return {
                'success': True,
                'products': [self._format_product(p) for p in products],
                'count': len(products),
                'category': category
            }
        except Exception as e:
            return {'success': False, 'error': f'Failed to load category: {e}'}
    
    def _format_product(self, product) -> Dict:
        """Format product for display"""
        return {
            'id': product.id,
            'name': product.name,
            'price': round(product.price, 2),
            'category': product.category,
            'stock': product.stock,
            'description': product.description,
            'is_available': product.is_available
        }
