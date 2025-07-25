"""Cart Controller - Simple coordinator for cart operations"""
from src.controllers.cart_operations import CartOperations
from src.controllers.cart_viewing import CartViewing


class CartController:
    def __init__(self, cart_service, user_controller):
        self.cart_ops = CartOperations(cart_service, user_controller)
        self.cart_viewing = CartViewing(cart_service, user_controller)
        self.user_controller = user_controller
    
    def _set_user(self, user_id):
        """Helper to set current user"""
        user = self.user_controller.user_service.get_user(user_id)
        # Set user in the auth component, not directly on user_controller
        self.user_controller.auth.current_user = user
    
    def add_to_cart(self, user_id, product_id, quantity=1):
        self._set_user(user_id)
        return self.cart_ops.add_to_cart(product_id, quantity)
    
    def remove_from_cart(self, user_id, product_id):
        self._set_user(user_id)
        return self.cart_ops.remove_from_cart(product_id)
    
    def update_quantity(self, user_id, product_id, quantity):
        self._set_user(user_id)
        return self.cart_ops.update_quantity(product_id, quantity)
    
    def clear_cart(self, user_id):
        self._set_user(user_id)
        return self.cart_ops.clear_cart()
    
    def view_cart(self, user_id):
        self._set_user(user_id)
        return self.cart_viewing.get_cart()
    
    def checkout(self, user_id):
        self._set_user(user_id)
        return self.cart_viewing.checkout()
    
    def get_cart_contents(self, user_id):
        self._set_user(user_id)
        return self.cart_viewing.get_cart()
    
    def get_cart_total(self, user_id):
        self._set_user(user_id)
        result = self.cart_viewing.get_cart()
        return result.get('total', 0) if result.get('success') else 0
    
    # Simplified methods for customer interface
    def add_item(self, product_id, quantity=1):
        """Add item to current user's cart"""
        current_user = self.user_controller.get_current_user()
        if not current_user:
            return {'success': False, 'error': 'No user logged in'}
        return self.cart_ops.add_to_cart(product_id, quantity)
    
    def remove_item(self, product_id):
        """Remove item from current user's cart"""
        current_user = self.user_controller.get_current_user()
        if not current_user:
            return {'success': False, 'error': 'No user logged in'}
        return self.cart_ops.remove_from_cart(product_id)
    
    def get_cart(self):
        """Get current user's cart"""
        current_user = self.user_controller.get_current_user()
        if not current_user:
            return {'success': False, 'error': 'No user logged in'}
        return self.cart_viewing.get_cart()
    
    def checkout_cart(self):
        """Checkout current user's cart"""
        current_user = self.user_controller.get_current_user()
        if not current_user:
            return {'success': False, 'error': 'No user logged in'}
        return self.cart_viewing.checkout()
