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
        if not self.user_controller.is_logged_in():
            return {'success': False, 'error': 'Please login first'}
        
        # Get current user
        current_user = self.user_controller.get_current_user()
        if not current_user:
            return {'success': False, 'error': 'No user logged in'}
            
        user_id = current_user['id']
        cart = self.cart_service.get_cart(user_id)
        
        if cart is not None:
            return {
                'success': True,
                'items': [self._format_cart_item(item) for item in cart.items],
                'total': self._calculate_total(cart.items),
                'count': len(cart.items)
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
        if not self.user_controller.is_logged_in():
            return {'success': False, 'error': 'Please login first'}
        
        # Get current user
        current_user = self.user_controller.get_current_user()
        if not current_user:
            return {'success': False, 'error': 'No user logged in'}
        
        # Get cart first to check if empty
        cart_result = self.get_cart()
        if not cart_result['success']:
            return cart_result
        
        if not cart_result['items']:
            return {
                'success': False,
                'error': 'Cannot checkout with empty cart'
            }
        
        user_id = current_user['id']
        checkout_result = self.cart_service.checkout(user_id)
        
        if checkout_result and checkout_result.get('success'):
            return {
                'success': True,
                'message': 'Checkout completed successfully!',
                'order_total': cart_result['total'],
                'order': checkout_result.get('order')
            }
        else:
            error_msg = 'Checkout failed'
            if checkout_result and checkout_result.get('error'):
                error_msg = checkout_result['error']
            return {
                'success': False,
                'error': error_msg
            }
    
    def _format_cart_item(self, item) -> Dict:
        """Format cart item for display"""
        subtotal = round(item.price_per_unit * item.quantity, 2)
        return {
            'product_id': item.product_id,
            'name': item.product_name,
            'price': round(item.price_per_unit, 2),
            'quantity': item.quantity,
            'subtotal': subtotal,
            'total': subtotal  # Add total field for compatibility
        }
    
    def _calculate_total(self, cart_items) -> float:
        """Calculate total price of cart items"""
        total = sum(item.price_per_unit * item.quantity for item in cart_items)
        return round(total, 2)
