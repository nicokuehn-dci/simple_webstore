"""
Cart Service - Business logic for shopping cart operations
"""
from typing import Optional, Dict
import uuid
import json
from pathlib import Path

from src.models.cart import Cart


class CartService:
    """Service for cart-related business operations"""

    def __init__(self, product_service, data_dir: str = "data"):
        """Initialize service with product service and data directory"""
        self.product_service = product_service
        self.active_carts: Dict[str, Cart] = {}
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        self.cart_file = self.data_dir / "carts.json"
        self._carts_loaded = False

    def save_all_carts(self):
        """Public method to save all carts"""
        self._save_carts()

    def _save_carts(self):
        """Save all active carts to disk"""
        cart_data = {}
        for user_id, cart in self.active_carts.items():
            cart_data[user_id] = {
                'user_id': cart.user_id,
                'created_at': cart.created_at.isoformat(),
                'items': [item.to_dict() for item in cart.items]
            }
        
        try:
            with open(self.cart_file, 'w', encoding='utf-8') as f:
                json.dump(cart_data, f, indent=2)
        except (IOError, OSError, ValueError) as e:
            print(f"Warning: Failed to save carts: {e}")

    def _load_carts(self):
        """Load saved carts from disk"""
        if not self.cart_file.exists():
            return
        
        try:
            with open(self.cart_file, 'r', encoding='utf-8') as f:
                cart_data = json.load(f)
            
            for user_id, data in cart_data.items():
                cart = Cart(user_id)
                # Restore cart items
                for item_data in data.get('items', []):
                    cart.add_item(
                        item_data['product_id'],
                        item_data['product_name'],
                        item_data['price_per_unit'],
                        item_data['quantity']
                    )
                self.active_carts[user_id] = cart
        except (IOError, OSError, ValueError) as e:
            print(f"Warning: Failed to load carts: {e}")

    def get_cart(self, user_id: str) -> Cart:
        """Get or create cart for user"""
        if user_id not in self.active_carts:
            # Try to load cart from disk first
            if not hasattr(self, '_carts_loaded'):
                self._load_carts()
                self._carts_loaded = True
            
            # If still not found, create new cart
            if user_id not in self.active_carts:
                self.active_carts[user_id] = Cart(user_id)
        
        return self.active_carts[user_id]

    def add_to_cart(self, user_id: str, product_id: str,
                    quantity: int = 1) -> bool:
        """Add product to user's cart"""
        # Get product details
        product = self.product_service.get_product_by_id(product_id)
        if not product:
            return False

        # Check stock availability
        if not product.is_available or product.stock < quantity:
            return False

        # Get user's cart
        cart = self.get_cart(user_id)

        # Add item to cart
        success = cart.add_item(
            product_id=product.id,
            product_name=product.name,
            price=product.price,
            quantity=quantity
        )
        
        # Automatically save cart after adding item
        if success:
            self._save_carts()
        
        return success

    def remove_from_cart(self, user_id: str, product_id: str) -> bool:
        """Remove product from user's cart"""
        cart = self.get_cart(user_id)
        success = cart.remove_item(product_id)
        
        # Automatically save cart after removing item
        if success:
            self._save_carts()
        
        return success

    def update_cart_item_quantity(self, user_id: str, product_id: str,
                                  new_quantity: int) -> bool:
        """Update quantity of item in cart"""
        if new_quantity < 0:
            return False

        # Check stock availability for the new quantity
        product = self.product_service.get_product_by_id(product_id)
        if product and new_quantity > product.stock:
            return False

        cart = self.get_cart(user_id)
        return cart.update_item_quantity(product_id, new_quantity)

    def clear_cart(self, user_id: str) -> bool:
        """Clear all items from user's cart"""
        cart = self.get_cart(user_id)
        cart.clear()
        
        # Automatically save cart after clearing
        self._save_carts()
        
        return True

    def get_cart_summary(self, user_id: str) -> dict:
        """Get cart summary with totals"""
        cart = self.get_cart(user_id)

        return {
            'user_id': user_id,
            'items': [item.to_dict() for item in cart.items],
            'total_amount': cart.get_total(),
            'item_count': cart.get_item_count(),
            'is_empty': cart.is_empty()
        }

    def validate_cart_stock(self, user_id: str) -> dict:
        """Validate that all cart items are still available"""
        cart = self.get_cart(user_id)
        issues = []

        for item in cart.items:
            product = self.product_service.get_product_by_id(item.product_id)

            if not product:
                issues.append(f"Product {item.product_name} no longer exists")
            elif not product.is_available:
                issues.append(f"Product {item.product_name} is out of stock")
            elif product.stock < item.quantity:
                issues.append(
                    f"Only {product.stock} of {item.product_name} available, "
                    f"but {item.quantity} in cart"
                )

        return {
            'valid': len(issues) == 0,
            'issues': issues
        }

    def checkout(self, user_id: str) -> Optional[dict]:
        """Process checkout for user's cart"""
        cart = self.get_cart(user_id)

        if cart.is_empty():
            return None

        # Validate stock availability
        validation = self.validate_cart_stock(user_id)
        if not validation['valid']:
            return {
                'success': False,
                'error': 'Stock validation failed',
                'issues': validation['issues']
            }

        # Create order summary
        order_id = self._generate_order_id()
        order_summary = {
            'order_id': order_id,
            'user_id': user_id,
            'items': [item.to_dict() for item in cart.items],
            'total_amount': cart.get_total(),
            'item_count': cart.get_item_count(),
            'status': 'completed',
            'created_at': cart.created_at.isoformat()
        }

        # Update stock levels
        for item in cart.items:
            product = self.product_service.get_product_by_id(item.product_id)
            if product:
                new_stock = product.stock - item.quantity
                self.product_service.update_stock(item.product_id, new_stock)

        # Clear cart after successful checkout
        cart.clear()
        
        # Automatically save cart after checkout
        self._save_carts()

        return {
            'success': True,
            'order': order_summary
        }

    def _generate_order_id(self) -> str:
        """Generate unique order ID"""
        return f"ORD-{str(uuid.uuid4())[:8].upper()}"
