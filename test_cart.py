#!/usr/bin/env python3
"""
Test cart functionality directly
"""
import sys
import os
from pathlib import Path

# Add src to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    from repositories.json_repository import JSONRepository
    from services.product_service import ProductService
    from services.cart_service import CartService
    from models.cart import Cart, CartItem
    
    print("✅ All imports successful")
    
    # Test CartItem creation
    item = CartItem(
        product_id="test123",
        product_name="Test Product",
        quantity=2,
        price_per_unit=10.99
    )
    print(f"✅ CartItem created: {item}")
    print(f"✅ CartItem dict: {item.to_dict()}")
    
    # Test Cart creation
    cart = Cart("user123")
    success = cart.add_item("test123", "Test Product", 10.99, 2)
    print(f"✅ Cart add_item success: {success}")
    print(f"✅ Cart items: {cart.items}")
    print(f"✅ Cart total: {cart.get_total()}")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
