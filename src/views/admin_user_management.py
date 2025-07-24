"""Admin User Management - User admin functions"""
from src.views.menu import SimpleMenu


def admin_user_menu(self):
    """Admin user management menu"""
    menu = SimpleMenu("👥 User Management", [
        "📋 List All Users",
        "🔄 Change User Role", 
        "🗑️ Delete User"
    ])
    
    choice = menu.display()
    
    if choice == 1:
        admin_list_users(self)
    elif choice == 2:
        admin_change_user_role(self)
    elif choice == 3:
        admin_delete_user(self)


def admin_list_users(interface):
    """Admin: List all users"""
    print("\n" + "=" * 60)
    print("👥 ALL USERS")
    print("=" * 60)
    
    result = interface.user_controller.list_users()
    
    if result['success']:
        users = result['users']
        
        if users:
            print(f"📊 Found {result['count']} user(s)\n")
            print(f"{'ID':<12} {'Username':<20} {'Email':<25} {'Role':<10}")
            print("-" * 75)
            
            for user in users:
                print(f"{user['id']:<12} {user['username']:<20} "
                      f"{user['email']:<25} {user['role']:<10}")
        else:
            print("No users found")
    else:
        print(f"❌ {result['error']}")
    
    input("\nPress Enter to continue...")


def admin_change_user_role(interface):
    """Admin: Change user role"""
    print("\n🔄 CHANGE USER ROLE")
    print("-" * 30)
    
    username = input("Username to modify: ").strip()
    if not username:
        return
    
    print("Available roles:")
    print("1. customer")
    print("2. admin")
    print("3. manager")
    
    try:
        role_choice = int(input("Select role (1-3): "))
        roles = ['customer', 'admin', 'manager']
        
        if 1 <= role_choice <= 3:
            new_role = roles[role_choice - 1]
            
            result = interface.user_controller.change_user_role(
                username, new_role
            )
            
            if result['success']:
                print(f"✅ {result['message']}")
            else:
                print(f"❌ {result['error']}")
        else:
            print("❌ Invalid role selection")
    except ValueError:
        print("❌ Invalid input")


def admin_delete_user(interface):
    """Admin: Delete user account"""
    print("\n🗑️ DELETE USER")
    print("-" * 20)
    
    username = input("Username to delete: ").strip()
    if not username:
        return
    
    confirm = input(f"Delete user '{username}'? (yes/no): ").strip().lower()
    
    if confirm == 'yes':
        result = interface.user_controller.delete_user(username)
        
        if result['success']:
            print(f"✅ {result['message']}")
        else:
            print(f"❌ {result['error']}")
    else:
        print("Delete cancelled")
