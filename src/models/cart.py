"""
Cart models - Shopping cart and cart item entities
"""
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional


@dataclass
class CartItem:
    """Individual item in shopping cart"""
    product_id: str
    product_name: str
    quantity: int
    price_per_unit: float
    
    def __post_init__(self):
        """Validate cart item data"""
        if self.quantity <= 0:
            raise ValueError("Quantity must be positive")
        if self.price_per_unit < 0:
            raise ValueError("Price cannot be negative")
    
    @property
    def total_price(self) -> float:
        """Calculate total price for this item"""
        return self.quantity * self.price_per_unit
    
    def to_dict(self) -> dict:
        """Convert cart item to dictionary"""
        return {
            'product_id': self.product_id,
            'product_name': self.product_name,
            'quantity': self.quantity,
            'price_per_unit': self.price_per_unit
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'CartItem':
        """Create cart item from dictionary"""
        return cls(
            product_id=data['product_id'],
            product_name=data['product_name'],
            quantity=data['quantity'],
            price_per_unit=data['price_per_unit']
        )
    
    def update_quantity(self, new_quantity: int) -> 'CartItem':
        """Return new cart item with updated quantity"""
        if new_quantity <= 0:
            raise ValueError("Quantity must be positive")
        
        return CartItem(
            product_id=self.product_id,
            product_name=self.product_name,
            quantity=new_quantity,
            price_per_unit=self.price_per_unit
        )


class Cart:
    """Shopping cart containing multiple items"""
    
    def __init__(self, user_id: str):
        """Initialize empty cart for user"""
        self.user_id = user_id
        self.items: List[CartItem] = []
        self.created_at = datetime.now()
    
    def add_item(self, product_id: str, product_name: str, 
                 price: float, quantity: int = 1) -> bool:
        """Add item to cart or update existing quantity"""
        try:
            # Check if item already exists
            for i, item in enumerate(self.items):
                if item.product_id == product_id:
                    # Update existing item
                    new_quantity = item.quantity + quantity
                    self.items[i] = item.update_quantity(new_quantity)
                    return True
            
            # Add new item
            new_item = CartItem(
                product_id=product_id,
                product_name=product_name,
                quantity=quantity,
                price_per_unit=price
            )
            self.items.append(new_item)
            return True
            
        except ValueError:
            return False
    
    def remove_item(self, product_id: str) -> bool:
        """Remove item from cart completely"""
        original_length = len(self.items)
        self.items = [item for item in self.items 
                     if item.product_id != product_id]
        return len(self.items) < original_length
    
    def update_item_quantity(self, product_id: str, 
                           new_quantity: int) -> bool:
        """Update quantity of specific item"""
        if new_quantity <= 0:
            return self.remove_item(product_id)
        
        for i, item in enumerate(self.items):
            if item.product_id == product_id:
                try:
                    self.items[i] = item.update_quantity(new_quantity)
                    return True
                except ValueError:
                    return False
        return False
    
    def get_total(self) -> float:
        """Calculate total cart value"""
        return sum(item.total_price for item in self.items)
    
    def get_item_count(self) -> int:
        """Get total number of items in cart"""
        return sum(item.quantity for item in self.items)
    
    def is_empty(self) -> bool:
        """Check if cart is empty"""
        return len(self.items) == 0
    
    def clear(self) -> None:
        """Remove all items from cart"""
        self.items.clear()
    
    def to_dict(self) -> dict:
        """Convert cart to dictionary for storage"""
        return {
            'user_id': self.user_id,
            'items': [item.to_dict() for item in self.items],
            'created_at': self.created_at.isoformat(),
            'total': self.get_total(),
            'item_count': self.get_item_count()
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Cart':
        """Create cart from dictionary"""
        cart = cls(data['user_id'])
        
        # Handle datetime conversion
        if data.get('created_at'):
            cart.created_at = datetime.fromisoformat(data['created_at'])
        
        # Load items
        for item_data in data.get('items', []):
            cart.items.append(CartItem.from_dict(item_data))
        
        return cart
    
    def __str__(self) -> str:
        """String representation for display"""
        if self.is_empty():
            return "🛒 Empty cart"
        return f"🛒 Cart: {self.get_item_count()} items, €{self.get_total():.2f}"
