"""
Cart Viewing - Handle cart display and checkout
"""
from typing import Dict
from src.services.cart_service import CartService


class CartViewing:
    """Handles cart viewing and checkout operations"""
    
    def __init__(self, cart_service: CartService, user_controller):
        self.cart_service = cart_service
        self.user_controller = user_controller
    
    def get_cart(self) -> Dict:
        """Get current user's cart contents"""
        auth_check = self.user_controller.require_login()
        if not auth_check['success']:
            return auth_check
        
        user_id = self.user_controller.current_user.id
        cart_items = self.cart_service.get_cart_contents(user_id)
        
        if cart_items is not None:
            return {
                'success': True,
                'items': [self._format_cart_item(item) for item in cart_items],
                'total': self._calculate_total(cart_items),
                'count': len(cart_items)
            }
        else:
            return {
                'success': False,
                'error': 'Failed to retrieve cart'
            }
    
    def get_cart_summary(self) -> Dict:
        """Get cart summary with totals"""
        cart_result = self.get_cart()
        
        if not cart_result['success']:
            return cart_result
        
        items = cart_result['items']
        
        return {
            'success': True,
            'summary': {
                'item_count': len(items),
                'total_quantity': sum(item['quantity'] for item in items),
                'subtotal': cart_result['total'],
                'total': cart_result['total']  # Could add tax, shipping, etc.
            }
        }
    
    def checkout(self) -> Dict:
        """Process checkout for current user"""
        auth_check = self.user_controller.require_login()
        if not auth_check['success']:
            return auth_check
        
        # Get cart first to check if empty
        cart_result = self.get_cart()
        if not cart_result['success']:
            return cart_result
        
        if not cart_result['items']:
            return {
                'success': False,
                'error': 'Cannot checkout with empty cart'
            }
        
        user_id = self.user_controller.current_user.id
        success = self.cart_service.checkout(user_id)
        
        if success:
            return {
                'success': True,
                'message': 'Checkout completed successfully!',
                'order_total': cart_result['total']
            }
        else:
            return {
                'success': False,
                'error': 'Checkout failed'
            }
    
    def _format_cart_item(self, item) -> Dict:
        """Format cart item for display"""
        return {
            'product_id': item.product.id,
            'name': item.product.name,
            'price': round(item.product.price, 2),
            'quantity': item.quantity,
            'subtotal': round(item.product.price * item.quantity, 2)
        }
    
    def _calculate_total(self, cart_items) -> float:
        """Calculate total price of cart items"""
        total = sum(item.product.price * item.quantity for item in cart_items)
        return round(total, 2)
