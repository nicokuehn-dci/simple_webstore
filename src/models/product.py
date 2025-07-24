"""
Product model - Simple, clean entity with validation
"""
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional


@dataclass
class Product:
    """Simple product entity with basic validation"""
    id: str
    name: str
    price: float
    category: str
    stock: int = 0
    description: str = ""
    created_at: Optional[datetime] = None
    
    def __post_init__(self):
        """Validate product data after initialization"""
        if self.created_at is None:
            self.created_at = datetime.now()
        
        # Basic validation
        if self.price < 0:
            raise ValueError("Price cannot be negative")
        if self.stock < 0:
            raise ValueError("Stock cannot be negative")
        if not self.name.strip():
            raise ValueError("Product name cannot be empty")
    
    @property
    def is_available(self) -> bool:
        """Check if product is in stock"""
        return self.stock > 0
    
    def to_dict(self) -> dict:
        """Convert product to dictionary for storage"""
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'category': self.category,
            'stock': self.stock,
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Product':
        """Create product from dictionary"""
        # Handle datetime conversion
        created_at = None
        if data.get('created_at'):
            created_at = datetime.fromisoformat(data['created_at'])
        
        return cls(
            id=data['id'],
            name=data['name'],
            price=data['price'],
            category=data['category'],
            stock=data.get('stock', 0),
            description=data.get('description', ''),
            created_at=created_at
        )
    
    def update_stock(self, new_stock: int) -> 'Product':
        """Return new product with updated stock"""
        if new_stock < 0:
            raise ValueError("Stock cannot be negative")
        
        return Product(
            id=self.id,
            name=self.name,
            price=self.price,
            category=self.category,
            stock=new_stock,
            description=self.description,
            created_at=self.created_at
        )
    
    def apply_discount(self, percentage: float) -> 'Product':
        """Return new product with discounted price"""
        if not 0 <= percentage <= 100:
            raise ValueError("Discount percentage must be between 0 and 100")
        
        new_price = self.price * (1 - percentage / 100)
        return Product(
            id=self.id,
            name=self.name,
            price=new_price,
            category=self.category,
            stock=self.stock,
            description=self.description,
            created_at=self.created_at
        )
    
    def __str__(self) -> str:
        """String representation for display"""
        status = "✅ Available" if self.is_available else "❌ Out of Stock"
        return f"{self.name} - €{self.price:.2f} ({self.category}) - {status}"
