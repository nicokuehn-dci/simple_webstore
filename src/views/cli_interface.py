"""Main CLI Interface - Simple coordinator"""
from .guest_interface import GuestInterface
from .customer_interface import CustomerInterface


class WebStoreInterface:
    def __init__(self, product_controller, user_controller, cart_controller):
        self.user_controller = user_controller
        self.guest_ui = GuestInterface(product_controller, user_controller)
        self.customer_ui = CustomerInterface(
            product_controller, user_controller, cart_controller
        )
    
    def run(self):
        """Main application loop"""
        
        while True:
            try:
                if not self.user_controller.is_logged_in():
                    if not self.guest_ui.show_guest_menu():
                        break
                else:
                    if not self.customer_ui.show_customer_menu():
                        break
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except (ValueError, TypeError, AttributeError,
                    ImportError, IOError) as e:
                print(f"Error: {e}")
                continue
            except SystemExit:
                break
    
    def print_welcome(self):
        """Display welcome message"""
        print("=" * 40)
        print("🛍️  SIMPLE WEBSTORE")
        print("=" * 40)
