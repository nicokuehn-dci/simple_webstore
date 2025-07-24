"""
Cart Operations - Basic cart add/remove operations
"""
from typing import Dict
from src.services.cart_service import CartService


class CartOperations:
    """Handles basic cart operations"""
    
    def __init__(self, cart_service: CartService, user_controller):
        self.cart_service = cart_service
        self.user_controller = user_controller
    
    def add_to_cart(self, product_id: str, quantity: int = 1) -> Dict:
        """Add product to current user's cart"""
        # Check authentication
        auth_check = self.user_controller.require_login()
        if not auth_check['success']:
            return auth_check
        
        # Validate input
        if quantity <= 0:
            return {'success': False, 'error': 'Quantity must be positive'}
        
        user_id = self.user_controller.current_user.id
        success = self.cart_service.add_to_cart(user_id, product_id, quantity)
        
        if success:
            return {
                'success': True,
                'message': f'Added {quantity} item(s) to cart'
            }
        else:
            return {
                'success': False,
                'error': 'Failed to add to cart (product not found or insufficient stock)'
            }
    
    def remove_from_cart(self, product_id: str) -> Dict:
        """Remove product from current user's cart"""
        auth_check = self.user_controller.require_login()
        if not auth_check['success']:
            return auth_check
        
        user_id = self.user_controller.current_user.id
        success = self.cart_service.remove_from_cart(user_id, product_id)
        
        if success:
            return {
                'success': True,
                'message': 'Item removed from cart'
            }
        else:
            return {
                'success': False,
                'error': 'Failed to remove item (not found in cart)'
            }
    
    def update_quantity(self, product_id: str, quantity: int) -> Dict:
        """Update quantity of item in cart"""
        auth_check = self.user_controller.require_login()
        if not auth_check['success']:
            return auth_check
        
        if quantity <= 0:
            return self.remove_from_cart(product_id)
        
        user_id = self.user_controller.current_user.id
        success = self.cart_service.update_quantity(user_id, product_id, quantity)
        
        if success:
            return {
                'success': True,
                'message': f'Updated quantity to {quantity}'
            }
        else:
            return {
                'success': False,
                'error': 'Failed to update quantity'
            }
    
    def clear_cart(self) -> Dict:
        """Clear all items from cart"""
        auth_check = self.user_controller.require_login()
        if not auth_check['success']:
            return auth_check
        
        user_id = self.user_controller.current_user.id
        success = self.cart_service.clear_cart(user_id)
        
        if success:
            return {
                'success': True,
                'message': 'Cart cleared successfully'
            }
        else:
            return {
                'success': False,
                'error': 'Failed to clear cart'
            }
