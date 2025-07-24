"""
Simple CLI Menu System - Clean and easy to use
"""
from typing import List, Optional
import sys


class SimpleMenu:
    """Simple menu system for CLI interface"""
    
    def __init__(self, title: str, options: List[str]):
        """Initialize menu with title and options"""
        self.title = title
        self.options = options
    
    def display(self) -> Optional[int]:
        """Display menu and get user choice"""
        print(f"\n{'=' * 60}")
        print(f"📋 {self.title}")
        print('=' * 60)
        
        for i, option in enumerate(self.options):
            print(f"  {i + 1}. {option}")
        print("  0. Exit/Back")
        print()
        
        try:
            choice = input("👉 Your choice: ").strip()
            if choice == '0':
                return None
            
            choice_num = int(choice) - 1
            if 0 <= choice_num < len(self.options):
                return choice_num
            else:
                print("❌ Invalid choice. Please try again.")
                input("Press Enter to continue...")
                return self.display()
                
        except ValueError:
            print("❌ Please enter a valid number.")
            input("Press Enter to continue...")
            return self.display()
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            sys.exit(0)
    
    def get_input(self, prompt: str, required: bool = True) -> str:
        """Get user input with validation"""
        while True:
            try:
                value = input(f"{prompt}: ").strip()
                if required and not value:
                    print("❌ This field is required.")
                    continue
                return value
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                sys.exit(0)
    
    def get_number_input(self, prompt: str, min_val: float | None = None,
                         max_val: float | None = None) -> float:
        """Get numeric input with validation"""
        while True:
            try:
                value_str = input(f"{prompt}: ").strip()
                value = float(value_str)
                
                if min_val is not None and value < min_val:
                    print(f"❌ Value must be at least {min_val}")
                    continue
                
                if max_val is not None and value > max_val:
                    print(f"❌ Value must be at most {max_val}")
                    continue
                
                return value
            except ValueError:
                print("❌ Please enter a valid number.")
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                sys.exit(0)
    
    def get_integer_input(self, prompt: str, min_val: int | None = None,
                          max_val: int | None = None) -> int:
        """Get integer input with validation"""
        return int(self.get_number_input(prompt, min_val, max_val))
    
    def confirm(self, message: str) -> bool:
        """Get yes/no confirmation from user"""
        while True:
            try:
                response = input(f"{message} (y/n): ").strip().lower()
                if response in ['y', 'yes']:
                    return True
                elif response in ['n', 'no']:
                    return False
                else:
                    print("❌ Please enter 'y' for yes or 'n' for no.")
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                sys.exit(0)
    
    @staticmethod
    def pause():
        """Pause and wait for user input"""
        try:
            input("\nPress Enter to continue...")
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            sys.exit(0)
    
    @staticmethod
    def clear_screen():
        """Clear the screen (works on most systems)"""
        import os
        os.system('cls' if os.name == 'nt' else 'clear')
    
    @staticmethod
    def print_success(message: str):
        """Print success message"""
        print(f"✅ {message}")
    
    @staticmethod
    def print_error(message: str):
        """Print error message"""
        print(f"❌ {message}")
    
    @staticmethod
    def print_info(message: str):
        """Print info message"""
        print(f"ℹ️  {message}")
    
    @staticmethod
    def print_separator():
        """Print a separator line"""
        print("-" * 60)
