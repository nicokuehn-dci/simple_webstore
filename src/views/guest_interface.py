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

        if choice == 1:
            self._register_user()
        elif choice == 2:
            self._login_user()
        elif choice == 3:
            self._browse_products_guest()
        elif choice == 4:
            self._search_products()
        elif choice == 5:
            self._show_about()
        elif choice == 0:
            return False  # Exit

        return True  # Continue

    def _register_user(self):
        """Handle user registration"""
        print("\n👥 USER REGISTRATION")
        print("-" * 30)

        username = input("Username: ").strip()
        email = input("Email: ").strip()

        result = self.user_controller.register(username, email)

        if result['success']:
            print(f"✅ {result['message']}")
            print("You can now login with your username.")
        else:
            print(f"❌ {result['error']}")

    def _login_user(self):
        """Handle user login"""
        print("\n🔑 USER LOGIN")
        print("-" * 20)

        username = input("Username: ").strip()

        result = self.user_controller.login(username)

        if result['success']:
            print(f"✅ {result['message']}")
        else:
            print(f"❌ {result['error']}")

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
