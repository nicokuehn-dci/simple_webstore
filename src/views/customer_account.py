"""Customer Account - Profile and account management"""


def view_cart(interface):
    """View shopping cart"""
    print("\n🛒 YOUR CART")
    print("-" * 20)
    
    current_user = interface.user_controller.get_current_user()
    if not current_user['success']:
        print("❌ Not logged in")
        return
    
    user_id = current_user['user']['id']
    result = interface.cart_controller.view_cart(user_id)
    
    if result.get('success'):
        items = result.get('items', [])
        if items:
            total = 0
            for item in items:
                item_total = item['price'] * item['quantity']
                total += item_total
                print(f"📦 {item['name']} - €{item['price']:.2f} "
                      f"x {item['quantity']} = €{item_total:.2f}")
            
            print(f"\n💰 Total: €{total:.2f}")
        else:
            print("Your cart is empty")
    else:
        print("❌ Could not load cart")
    
    input("Press Enter to continue...")


def checkout(interface):
    """Process checkout"""
    print("\n💳 CHECKOUT")
    print("-" * 15)
    
    current_user = interface.user_controller.get_current_user()
    if not current_user['success']:
        print("❌ Not logged in")
        return
    
    user_id = current_user['user']['id']
    
    # Show cart first
    cart_result = interface.cart_controller.view_cart(user_id)
    if not cart_result.get('success') or not cart_result.get('items'):
        print("Your cart is empty")
        return
    
    items = cart_result['items']
    total = sum(item['price'] * item['quantity'] for item in items)
    
    print("Order summary:")
    for item in items:
        item_total = item['price'] * item['quantity']
        print(f"• {item['name']} x {item['quantity']} = €{item_total:.2f}")
    
    print(f"\n💰 Total: €{total:.2f}")
    
    confirm = input("\nConfirm order? (yes/no): ").strip().lower()
    
    if confirm == 'yes':
        result = interface.cart_controller.checkout(user_id)
        
        if result['success']:
            print(f"✅ {result['message']}")
        else:
            print(f"❌ {result['error']}")
    else:
        print("Order cancelled")


def view_profile(interface):
    """View user profile"""
    print("\n👤 YOUR PROFILE")
    print("-" * 20)
    
    result = interface.user_controller.get_current_user()
    
    if result['success']:
        user = result['user']
        print(f"Username: {user['username']}")
        print(f"Email: {user['email']}")
        print(f"Role: {user['role']}")
        print(f"Member since: {user.get('created_at', 'Unknown')}")
    else:
        print(f"❌ {result['error']}")
    
    input("Press Enter to continue...")


def logout_user(interface):
    """Logout current user"""
    result = interface.user_controller.logout()
    
    if result['success']:
        print(f"✅ {result['message']}")
    else:
        print(f"❌ {result['error']}")
    
    return False  # Exit customer menu
