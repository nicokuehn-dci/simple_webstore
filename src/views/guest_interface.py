"""
Guest Interface - Handles non-logged-in user interactions
"""
from src.views.menu import SimpleMenu


class GuestInterface:
    """Interface for guest (non-logged-in) users"""

    def __init__(self, product_controller, user_controller):
        self.product_controller = product_controller
        self.user_controller = user_controller

    def show_guest_menu(self):
        """Menu for non-logged-in users"""
        menu = SimpleMenu("Welcome - Please Login or Register", [
            "👥 Register New Account",
            "🔑 Login to Existing Account",
            "👀 Browse Products (Guest Mode)",
            "🔍 Search Products",
            "ℹ️  About This Application"
        ])

        choice = menu.display()

        if choice == 0:  # Register New Account (Index 0 = Option 1)
            self._register_user()
        elif choice == 1:  # Login to Existing Account (Index 1 = Option 2)
            self._login_user()
        elif choice == 2:  # Browse Products (Index 2 = Option 3)
            self._browse_products_guest()
        elif choice == 3:  # Search Products (Index 3 = Option 4)
            self._search_products()
        elif choice == 4:  # About This Application (Index 4 = Option 5)
            self._show_about()
        elif choice is None:  # Exit/Back (User chose 0)
            return False  # Exit

        return True  # Continue

    def _register_user(self):
        """Handle user registration"""
        print("\n👥 USER REGISTRATION")
        print("-" * 30)

        # Get username
        username = input("Username: ").strip()
        if not username:
            print("do you wanna kidding me ? Enter correct data :-)")
            input("Press Enter to continue...")
            return

        # Get and validate email
        email = input("Email: ").strip()
        if not self._validate_email(email):
            print("do you wanna kidding me ? Enter correct data :-)")
            input("Press Enter to continue...")
            return

        # Get password
        import getpass
        password = getpass.getpass("Password: ")
        if not password:
            print("do you wanna kidding me ? Enter correct data :-)")
            input("Press Enter to continue...")
            return

        # Confirm password
        password_confirm = getpass.getpass("Confirm Password: ")
        if password != password_confirm:
            print("do you wanna kidding me ? Enter correct data :-)")
            print("Passwords do not match!")
            input("Press Enter to continue...")
            return

        result = self.user_controller.register(username, email, password)

        if result['success']:
            print(f"✅ {result['message']}")
            print("You can now login with your username and password.")
            input("Press Enter to continue...")
        else:
            print(f"❌ {result['error']}")
            input("Press Enter to continue...")

    def _validate_email(self, email: str) -> bool:
        """Validate email format"""
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))

    def _login_user(self):
        """Handle user login"""
        print("\n🔑 USER LOGIN")
        print("-" * 20)

        username = input("Username: ").strip()
        
        if not username:
            print("do you wanna kidding me ? Enter correct data :-)")
            input("Press Enter to continue...")
            return

        # Get password
        import getpass
        password = getpass.getpass("Password: ")
        
        if not password:
            print("do you wanna kidding me ? Enter correct data :-)")
            input("Press Enter to continue...")
            return

        result = self.user_controller.login(username, password)

        if result['success']:
            print(f"✅ {result['message']}")
            if result.get('is_admin'):
                print("🔑 Admin privileges detected!")
            input("Press Enter to continue...")
        else:
            print(f"❌ {result['error']}")
            print("💡 Tip: Try 'admin'/'admin123' or 'customer'/'customer123'")
            print("   for demo accounts")
            input("Press Enter to continue...")

    def _browse_products_guest(self):
        """Browse products without login"""
        print("\n👀 PRODUCT CATALOG (Guest Mode)")
        print("-" * 40)

        result = self.product_controller.list_products()

        if result['success']:
            for product in result['products']:
                print(f"📦 {product['name']} - €{product['price']:.2f}")
                category = product['category']
                stock = product['stock']
                print(f"   Category: {category} | Stock: {stock}")
                print()
        else:
            print(f"❌ {result['error']}")

    def _search_products(self):
        """Search products"""
        print("\n🔍 PRODUCT SEARCH")
        print("-" * 25)

        query = input("Search term: ").strip()

        if query:
            result = self.product_controller.search_products(query)

            if result['success'] and result['products']:
                print(f"\n Found {len(result['products'])} products:")
                for product in result['products']:
                    print(f"📦 {product['name']} - €{product['price']:.2f}")
            else:
                print("No products found.")

    def _show_about(self):
        """Show application information"""
        print("\n" + "=" * 50)
        print("ℹ️  ABOUT SIMPLE WEBSTORE")
        print("=" * 50)
        print("A clean, educational e-commerce CLI application")
        print("demonstrating modern software architecture.")
        print()
        print("Features:")
        print("• MVC Architecture Pattern")
        print("• Repository Pattern for Data Storage")
        print("• Clean Code Principles")
        print("• Modular Component Design")
        print("=" * 50)
