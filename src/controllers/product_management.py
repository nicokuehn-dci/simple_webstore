"""
Product Management - Admin operations for products
"""
from typing import Dict
from src.services.product_service import ProductService


class ProductManagement:
    """Handles admin product management operations"""

    def __init__(self, product_service: ProductService):
        self.product_service = product_service

    def get_low_stock_products(self, threshold: int = 5) -> Dict:
        """Get products with low stock"""
        try:
            products = self.product_service.get_low_stock_products(threshold)
            return {
                'success': True,
                'products': [self._format_product(p) for p in products],
                'count': len(products),
                'threshold': threshold
            }
        except (ValueError, TypeError, IOError) as e:
            return {'success': False, 'error': f'Failed to check stock: {e}'}

    def apply_category_discount(self, category: str,
                                discount_percent: float) -> Dict:
        """Apply discount to all products in category"""
        if not 0 <= discount_percent <= 100:
            error_msg = 'Discount must be between 0 and 100'
            return {'success': False, 'error': error_msg}

        try:
            updated_count = self.product_service.apply_discount_to_category(
                category, discount_percent
            )
            return {
                'success': True,
                'message': (f'Applied {discount_percent}% discount to '
                            f'{updated_count} products'),
                'updated_count': updated_count
            }
        except (ValueError, TypeError, IOError) as e:
            error_msg = f'Failed to apply discount: {e}'
            return {'success': False, 'error': error_msg}
    
    def get_product_stats(self) -> Dict:
        """Get product statistics"""
        try:
            all_products = self.product_service.get_all_products()
            total_products = len(all_products)
            total_value = sum(p.price * p.stock for p in all_products)
            low_stock_count = len([p for p in all_products if p.stock <= 5])
            out_of_stock_count = len([p for p in all_products if p.stock == 0])
            
            return {
                'success': True,
                'stats': {
                    'total_products': total_products,
                    'total_value': round(total_value, 2),
                    'low_stock_count': low_stock_count,
                    'out_of_stock_count': out_of_stock_count
                }
            }
        except (ValueError, TypeError, IOError) as e:
            return {'success': False, 'error': f'Failed to get stats: {e}'}

    def bulk_update_stock(self, updates: Dict[str, int]) -> Dict:
        """Update stock for multiple products"""
        try:
            updated_count = 0
            for product_id, new_stock in updates.items():
                success = self.product_service.update_product(
                    product_id, stock=new_stock)
                if success:
                    updated_count += 1

            return {
                'success': True,
                'message': f'Updated stock for {updated_count} products',
                'updated_count': updated_count
            }
        except (ValueError, TypeError, IOError) as e:
            return {'success': False, 'error': f'Bulk update failed: {e}'}

    def _format_product(self, product) -> Dict:
        """Format product for display"""
        return {
            'id': product.id,
            'name': product.name,
            'price': round(product.price, 2),
            'category': product.category,
            'stock': product.stock,
            'is_available': product.is_available
        }
