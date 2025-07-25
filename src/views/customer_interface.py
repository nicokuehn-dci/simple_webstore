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
        
        # Check if user is admin and add admin options
        if self.user_controller.is_admin():
            menu_title = f"Admin Panel - Welcome {user['username']}"
            menu_options = [
                "📦 Browse Products",
                "🛒 View My Cart",
                "➕ Add Product to Cart",
                "➖ Remove from Cart",
                "💳 Checkout",
                "👤 My Profile",
                "👑 Admin: Manage Products",
                "👑 Admin: Manage Users",
                "🔓 Logout"
            ]
        else:
            menu_title = f"Customer Panel - Welcome {user['username']}"
            menu_options = [
                "📦 Browse Products",
                "🛒 View My Cart",
                "➕ Add Product to Cart",
                "➖ Remove from Cart",
                "💳 Checkout",
                "👤 My Profile",
                "🔓 Logout"
            ]
        
        menu = SimpleMenu(menu_title, menu_options)
        choice = menu.display()
        
        if choice == 0:  # Browse Products (Index 0 = Option 1)
            self._browse_products()
        elif choice == 1:  # View My Cart (Index 1 = Option 2)
            self._view_cart()
        elif choice == 2:  # Add Product to Cart (Index 2 = Option 3)
            self._add_to_cart()
        elif choice == 3:  # Remove from Cart (Index 3 = Option 4)
            self._remove_from_cart()
        elif choice == 4:  # Checkout (Index 4 = Option 5)
            self._checkout()
        elif choice == 5:  # My Profile (Index 5 = Option 6)
            self._view_profile()
        elif choice == 6:  # Admin or Logout depending on user type
            if self.user_controller.is_admin():
                self._admin_manage_products()
            else:
                return self._logout()  # Logout for regular customers
        elif choice == 7:  # Admin: Manage Users (Admin only)
            if self.user_controller.is_admin():
                self._admin_manage_users()
            else:
                return False
        elif choice == 8:  # Logout (Admin only - extra option)
            if self.user_controller.is_admin():
                return self._logout()
            else:
                return False
        elif choice is None:  # Exit/Back (User chose 0)
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
                product_info = f"{product['id']}. {product['name']}"
                price_info = f"€{product['price']:.2f}"
                print(f"{product_info} - {price_info}")
                category = product['category']
                stock = product['stock']
                print(f"   Category: {category} | Stock: {stock} {status}")
                print()
        else:
            print(f"❌ {result['error']}")
    
    def _view_cart(self):
        """View shopping cart"""
        print("🔍 DEBUG: Getting cart...")
        result = self.cart_controller.get_cart()
        print(f"🔍 DEBUG: Cart result = {result}")
        
        if result['success'] and result['items']:
            print("\n🛒 YOUR SHOPPING CART")
            print("-" * 35)
            
            total = 0
            for item in result['items']:
                subtotal = item['price'] * item['quantity']
                total += subtotal
                quantity_name = f"{item['quantity']}x {item['name']}"
                price_text = f"€{subtotal:.2f}"
                print(f"• {quantity_name} - {price_text}")
            
            print(f"\nTotal: €{total:.2f}")
        elif result['success'] and not result['items']:
            print("\n🛒 Your cart is empty!")
            print("🔍 DEBUG: Cart is empty - no items found")
        else:
            print("\n🛒 Your cart is empty!")
            print(f"🔍 DEBUG: Cart failed - Error: {result.get('error', 'Unknown error')}")
        
        input("Press Enter to continue...")
    
    def _add_to_cart(self):
        """Add product to cart"""
        print("\n➕ ADD TO CART")
        print("-" * 20)
        
        # Get all products first
        result = self.product_controller.list_products()
        
        if not result['success'] or not result['products']:
            print("❌ No products available!")
            input("Press Enter to continue...")
            return
            
        products = result['products']
        
        # Display products with numbers
        print("📦 Available Products:")
        print("-" * 40)
        for i, product in enumerate(products, 1):
            print(f"  {i}. {product['name']} - €{product['price']:.2f}")
            print(f"     Category: {product['category']} | "
                  f"Stock: {product['stock']}")
            print()
        
        try:
            choice = input("👉 Select product number (0 to cancel): ").strip()
            
            if choice == "0":
                return
                
            product_index = int(choice) - 1
            
            if 0 <= product_index < len(products):
                selected_product = products[product_index]
                
                # Check stock
                if selected_product['stock'] <= 0:
                    print(f"❌ Product '{selected_product['name']}' "
                          f"is out of stock!")
                    input("Press Enter to continue...")
                    return
                
                print(f"Selected: {selected_product['name']} - "
                      f"€{selected_product['price']:.2f}")
                max_qty = selected_product['stock']
                
                prompt = f"Quantity (1-{max_qty}, default 1): "
                quantity_input = input(prompt).strip()
                quantity = int(quantity_input) if quantity_input else 1
                
                if quantity < 1 or quantity > max_qty:
                    print("do you wanna kidding me ? Enter correct data :-)")
                    print(f"Quantity must be between 1 and {max_qty}")
                    input("Press Enter to continue...")
                    return
                
                # Add to cart using product ID
                print(f"🔍 DEBUG: Adding product {selected_product['id']} "
                      f"quantity {quantity} to cart...")
                result = self.cart_controller.add_item(
                    selected_product['id'], quantity)
                print(f"🔍 DEBUG: Add to cart result = {result}")
                
                if result['success']:
                    print(f"✅ Added {quantity}x {selected_product['name']} "
                          f"to cart!")
                else:
                    print(f"❌ {result['error']}")
            else:
                print("do you wanna kidding me ? Enter correct data :-)")
                
        except ValueError:
            print("do you wanna kidding me ? Enter correct data :-)")
        
        input("Press Enter to continue...")
    
    def _remove_from_cart(self):
        """Remove product from cart"""
        print("\n➖ REMOVE FROM CART")
        print("-" * 25)
        
        # First show current cart
        cart_result = self.cart_controller.get_cart()
        
        if not cart_result['success'] or not cart_result['items']:
            print("❌ Your cart is empty!")
            input("Press Enter to continue...")
            return
        
        cart_items = cart_result['items']
        
        # Display cart items with numbers
        print("🛒 Items in your cart:")
        print("-" * 30)
        for i, item in enumerate(cart_items, 1):
            print(f"  {i}. {item['name']} - €{item['price']:.2f}")
            print(f"     Quantity: {item['quantity']} | "
                  f"Total: €{item['total']:.2f}")
            print()
        
        try:
            prompt = "👉 Select item number to remove (0 to cancel): "
            choice = input(prompt).strip()
            
            if choice == "0":
                return
                
            item_index = int(choice) - 1
            
            if 0 <= item_index < len(cart_items):
                selected_item = cart_items[item_index]
                
                # Confirm removal
                item_name = selected_item['name']
                confirm_msg = f"Remove {item_name} from cart? (y/n): "
                confirm = input(confirm_msg).strip().lower()
                
                if confirm in ['y', 'yes']:
                    result = self.cart_controller.remove_item(
                        selected_item['product_id'])
                    
                    if result['success']:
                        print(f"✅ Removed {selected_item['name']} from cart!")
                    else:
                        print(f"❌ {result['error']}")
                else:
                    print("❌ Removal cancelled.")
            else:
                print("do you wanna kidding me ? Enter correct data :-)")
                
        except ValueError:
            print("do you wanna kidding me ? Enter correct data :-)")
        
        input("Press Enter to continue...")
    
    def _checkout(self):
        """Process checkout"""
        result = self.cart_controller.get_cart()
        
        if not result['success'] or not result['items']:
            print("❌ Your cart is empty!")
            return
        
        # Show cart summary
        self._view_cart()
        
        if input("\nProceed with checkout? (y/n): ").lower() == 'y':
            checkout_result = self.cart_controller.checkout_cart()
            
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
        if result['success']:
            print(f"✅ {result['message']}")
        else:
            print(f"❌ {result['error']}")
        input("Press Enter to continue...")
        return False  # Return to guest menu
    
    def _admin_manage_products(self):
        """Admin: Manage products"""
        print("\n👑 ADMIN: Product Management")
        print("-" * 35)
        print("1. Add New Product")
        print("2. List All Products")
        print("3. Update Product")
        print("4. Delete Product")
        print("0. Back")
        
        choice = input("👉 Choice: ").strip()
        
        if choice == "1":
            self._admin_add_product()
        elif choice == "2":
            self._browse_products()
        elif choice == "3":
            print("⚠️  Update Product feature coming soon!")
            input("Press Enter to continue...")
        elif choice == "4":
            print("⚠️  Delete Product feature coming soon!")
            input("Press Enter to continue...")
    
    def _admin_add_product(self):
        """Admin: Add new product"""
        print("\n➕ ADD NEW PRODUCT")
        print("-" * 20)
        
        name = input("Product Name: ").strip()
        if not name:
            print("❌ Product name required!")
            input("Press Enter to continue...")
            return
            
        try:
            price = float(input("Price: €").strip())
            stock = int(input("Stock quantity: ").strip())
        except ValueError:
            print("do you wanna kidding me ? Enter correct data :-)")
            input("Press Enter to continue...")
            return
            
        category = input("Category: ").strip()
        description = input("Description (optional): ").strip()
        
        result = self.product_controller.create_product(
            name=name,
            price=price,
            category=category or "General",
            stock=stock,
            description=description
        )
        
        if result['success']:
            print(f"✅ Product '{name}' added successfully!")
        else:
            print(f"❌ {result['error']}")
        
        input("Press Enter to continue...")
    
    def _admin_manage_users(self):
        """Admin: Manage users"""
        print("\n👑 ADMIN: User Management")
        print("-" * 30)
        print("1. List All Users")
        print("2. Create New User")
        print("0. Back")
        
        choice = input("👉 Choice: ").strip()
        
        if choice == "1":
            self._admin_list_users()
        elif choice == "2":
            print("⚠️  Create User feature coming soon!")
            input("Press Enter to continue...")
    
    def _admin_list_users(self):
        """Admin: List all users"""
        print("\n👥 ALL USERS")
        print("-" * 15)
        
        # This would need to be implemented in the user controller
        print("Admin users list feature needs backend implementation")
        input("Press Enter to continue...")
