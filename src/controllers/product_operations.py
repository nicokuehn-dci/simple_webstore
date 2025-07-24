"""
Product Operations - Basic CRUD operations for products
"""
from typing import Dict
from src.services.product_service import ProductService


class ProductOperations:
    """Handles basic product CRUD operations"""
    
    def __init__(self, product_service: ProductService):
        self.product_service = product_service
    
    def create_product(self, name: str, price: float, category: str,
                      stock: int = 0, description: str = "") -> Dict:
        """Create a new product"""
        if not name.strip():
            return {'success': False, 'error': 'Product name is required'}
        
        if price < 0:
            return {'success': False, 'error': 'Price cannot be negative'}
        
        if stock < 0:
            return {'success': False, 'error': 'Stock cannot be negative'}
        
        product = self.product_service.create_product(
            name=name,
            price=price,
            category=category,
            stock=stock,
            description=description
        )
        
        if product:
            return {
                'success': True,
                'product': self._format_product(product),
                'message': f'Product "{name}" created successfully'
            }
        else:
            return {'success': False, 'error': 'Failed to create product'}
    
    def update_product(self, product_id: str, **kwargs) -> Dict:
        """Update product information"""
        # Check if product exists
        if not self.product_service.get_product_by_id(product_id):
            return {'success': False, 'error': 'Product not found'}
        
        # Validate input
        if 'price' in kwargs and kwargs['price'] < 0:
            return {'success': False, 'error': 'Price cannot be negative'}
        
        if 'stock' in kwargs and kwargs['stock'] < 0:
            return {'success': False, 'error': 'Stock cannot be negative'}
        
        success = self.product_service.update_product(product_id, **kwargs)
        
        if success:
            updated_product = self.product_service.get_product_by_id(product_id)
            return {
                'success': True,
                'product': self._format_product(updated_product),
                'message': 'Product updated successfully'
            }
        else:
            return {'success': False, 'error': 'Failed to update product'}
    
    def delete_product(self, product_id: str) -> Dict:
        """Delete a product"""
        # Check if product exists
        product = self.product_service.get_product_by_id(product_id)
        if not product:
            return {'success': False, 'error': 'Product not found'}
        
        success = self.product_service.delete_product(product_id)
        
        if success:
            return {
                'success': True,
                'message': f'Product "{product.name}" deleted successfully'
            }
        else:
            return {'success': False, 'error': 'Failed to delete product'}
    
    def _format_product(self, product) -> Dict:
        """Format product for display"""
        return {
            'id': product.id,
            'name': product.name,
            'price': round(product.price, 2),
            'price_display': f"€{product.price:.2f}",
            'category': product.category,
            'stock': product.stock,
            'description': product.description,
            'is_available': product.is_available,
            'status': "✅ Available" if product.is_available else "❌ Out of Stock",
            'created_at': product.created_at.isoformat() if product.created_at else None
        }
