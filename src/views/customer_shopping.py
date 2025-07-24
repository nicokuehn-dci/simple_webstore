"""Customer Shopping - Product browsing and shopping functions"""
from src.views.menu import SimpleMenu


def browse_products(interface):
    """Browse all products"""
    print("\n🛒 PRODUCT CATALOG")
    print("-" * 30)
    
    result = interface.product_controller.list_products()
    
    if result['success']:
        for product in result['products']:
            print(f"📦 {product['name']} - €{product['price']:.2f}")
            print(f"   Category: {product['category']} | Stock: {product['stock']}")
            if product.get('description'):
                print(f"   {product['description']}")
            print()
    else:
        print(f"❌ {result['error']}")
    
    input("Press Enter to continue...")


def add_to_cart(interface):
    """Add product to cart"""
    print("\n➕ ADD TO CART")
    print("-" * 20)
    
    result = interface.product_controller.list_products()
    if not result['success']:
        print(f"❌ {result['error']}")
        return
    
    products = result['products']
    if not products:
        print("No products available")
        return
    
    print("Available products:")
    for i, product in enumerate(products, 1):
        print(f"{i}. {product['name']} - €{product['price']:.2f} "
              f"(Stock: {product['stock']})")
    
    try:
        choice = int(input("\nSelect product (number): "))
        if 1 <= choice <= len(products):
            product = products[choice - 1]
            quantity = int(input("Quantity: "))
            
            if quantity > 0:
                current_user = interface.user_controller.get_current_user()
                if current_user['success']:
                    user_id = current_user['user']['id']
                    result = interface.cart_controller.add_to_cart(
                        user_id, product['id'], quantity
                    )
                    
                    if result['success']:
                        print(f"✅ {result['message']}")
                    else:
                        print(f"❌ {result['error']}")
            else:
                print("❌ Quantity must be positive")
        else:
            print("❌ Invalid selection")
    except ValueError:
        print("❌ Invalid input")


def remove_from_cart(interface):
    """Remove product from cart"""
    print("\n🗑️ REMOVE FROM CART")
    print("-" * 25)
    
    current_user = interface.user_controller.get_current_user()
    if not current_user['success']:
        print("❌ Not logged in")
        return
    
    user_id = current_user['user']['id']
    cart_result = interface.cart_controller.view_cart(user_id)
    
    if not cart_result.get('success'):
        print("Cart is empty")
        return
    
    cart_items = cart_result.get('items', [])
    if not cart_items:
        print("Cart is empty")
        return
    
    print("Cart contents:")
    for i, item in enumerate(cart_items, 1):
        print(f"{i}. {item['name']} - Qty: {item['quantity']}")
    
    try:
        choice = int(input("\nSelect item to remove (number): "))
        if 1 <= choice <= len(cart_items):
            item = cart_items[choice - 1]
            
            result = interface.cart_controller.remove_from_cart(
                user_id, item['product_id']
            )
            
            if result['success']:
                print(f"✅ {result['message']}")
            else:
                print(f"❌ {result['error']}")
        else:
            print("❌ Invalid selection")
    except ValueError:
        print("❌ Invalid input")
