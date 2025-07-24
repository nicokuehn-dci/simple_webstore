"""
Customer Interface - Handles logged-in customer interactions
"""
from src.views.menu import SimpleMenu


class CustomerInterface:
    """Interface for logged-in customers"""
    
    def __init__(self, product_controller, user_controller, cart_controller):
        self.product_controller = product_controller
        self.user_controller = user_controller
        self.cart_controller = cart_controller
    
    def show_customer_menu(self):
        """Menu for logged-in customers"""
        user = self.user_controller.get_current_user()
        
        menu = SimpleMenu(f"Customer Panel - Welcome {user['username']}", [
            "📦 Browse Products",
            "🛒 View My Cart",
            "➕ Add Product to Cart",
            "➖ Remove from Cart",
            "💳 Checkout",
            "👤 My Profile",
            "🔓 Logout"
        ])
        
        choice = menu.display()
        
        if choice == 1:
            self._browse_products()
        elif choice == 2:
            self._view_cart()
        elif choice == 3:
            self._add_to_cart()
        elif choice == 4:
            self._remove_from_cart()
        elif choice == 5:
            self._checkout()
        elif choice == 6:
            self._view_profile()
        elif choice == 7:
            self._logout()
        elif choice == 0:
            return False
        
        return True
    
    def _browse_products(self):
        """Browse all products"""
        print("\n📦 PRODUCT CATALOG")
        print("-" * 30)
        
        result = self.product_controller.list_products()
        
        if result['success']:
            for product in result['products']:
                status = "✅" if product['stock'] > 0 else "❌ Out of Stock"
                print(f"{product['id']}. {product['name']} - €{product['price']:.2f}")
                print(f"   Category: {product['category']} | Stock: {product['stock']} {status}")
                print()
        else:
            print(f"❌ {result['error']}")
    
    def _view_cart(self):
        """View shopping cart"""
        result = self.cart_controller.get_cart()
        
        if result['success'] and result['items']:
            print("\n🛒 YOUR SHOPPING CART")
            print("-" * 35)
            
            total = 0
            for item in result['items']:
                subtotal = item['price'] * item['quantity']
                total += subtotal
                print(f"• {item['quantity']}x {item['name']} - €{subtotal:.2f}")
            
            print(f"\nTotal: €{total:.2f}")
        else:
            print("\n🛒 Your cart is empty!")
    
    def _add_to_cart(self):
        """Add product to cart"""
        print("\n➕ ADD TO CART")
        print("-" * 20)
        
        try:
            product_id = int(input("Product ID: "))
            quantity = int(input("Quantity (default 1): ") or "1")
            
            result = self.cart_controller.add_item(product_id, quantity)
            
            if result['success']:
                print(f"✅ {result['message']}")
            else:
                print(f"❌ {result['error']}")
                
        except ValueError:
            print("❌ Invalid input!")
    
    def _remove_from_cart(self):
        """Remove product from cart"""
        print("\n➖ REMOVE FROM CART")
        print("-" * 25)
        
        try:
            product_id = int(input("Product ID to remove: "))
            
            result = self.cart_controller.remove_item(product_id)
            
            if result['success']:
                print(f"✅ {result['message']}")
            else:
                print(f"❌ {result['error']}")
                
        except ValueError:
            print("❌ Invalid input!")
    
    def _checkout(self):
        """Process checkout"""
        result = self.cart_controller.get_cart()
        
        if not result['success'] or not result['items']:
            print("❌ Your cart is empty!")
            return
        
        # Show cart summary
        self._view_cart()
        
        if input("\nProceed with checkout? (y/n): ").lower() == 'y':
            checkout_result = self.cart_controller.checkout()
            
            if checkout_result['success']:
                print("✅ Order placed successfully! Thank you for shopping!")
            else:
                print(f"❌ {checkout_result['error']}")
        else:
            print("❌ Checkout cancelled")
    
    def _view_profile(self):
        """View user profile"""
        result = self.user_controller.get_user_profile()
        
        if result['success']:
            profile = result['profile']
            print("\n👤 YOUR PROFILE")
            print("-" * 20)
            print(f"Username: {profile['username']}")
            print(f"Email: {profile['email']}")
            print(f"Role: {profile['role']}")
        else:
            print(f"❌ {result['error']}")
    
    def _logout(self):
        """Logout user"""
        result = self.user_controller.logout()
        print(f"✅ {result['message']}")
