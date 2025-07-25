"""
Admin interface extensions for CLI
"""


def _admin_product_menu(self):
    """Admin product management menu"""
    from src.views.menu import SimpleMenu

    menu = SimpleMenu("Product Management", [
        "➕ Add New Product",
        "📋 List All Products",
        "📝 Update Product",
        "🗑️  Delete Product",
        "📊 Low Stock Report",
        "🏷️  Apply Category Discount"
    ])

    choice = menu.display()
    if choice is None:
        return
    elif choice == 0:
        self._admin_add_product()
    elif choice == 1:
        self._browse_products()
    elif choice == 2:
        self._admin_update_product()
    elif choice == 3:
        self._admin_delete_product()
    elif choice == 4:
        self._admin_low_stock_report()
    elif choice == 5:
        self._admin_category_discount()


def _admin_add_product(self):
    """Admin: Add new product"""
    print("\n" + "=" * 50)
    print("➕ ADD NEW PRODUCT")
    print("=" * 50)

    name = self.menu.get_input("Product Name")
    price = self.menu.get_number_input("Price (€)", min_val=0)
    category = self.menu.get_input("Category")
    stock = self.menu.get_integer_input("Initial Stock", min_val=0)
    description = self.menu.get_input("Description (optional)", required=False)

    result = self.product_controller.create_product(
        name=name,
        price=price,
        category=category,
        stock=stock,
        description=description
    )

    if result['success']:
        self.menu.print_success(result['message'])
        product = result['product']
        print(f"   ID: {product['id']}")
        print(f"   Name: {product['name']}")
        print(f"   Price: {product['price_display']}")
    else:
        self.menu.print_error(result['error'])

    self.menu.pause()


def _admin_update_product(self):
    """Admin: Update existing product"""
    print("\n" + "=" * 50)
    print("📝 UPDATE PRODUCT")
    print("=" * 50)

    product_id = self.menu.get_input("Product ID to update")

    # Check if product exists
    product_result = self.product_controller.get_product(product_id)
    if not product_result['success']:
        self.menu.print_error(product_result['error'])
        self.menu.pause()
        return

    product = product_result['product']
    print(f"\nCurrent product: {product['name']} - {product['price_display']}")
    print("Leave fields empty to keep current values:")

    # Get new values
    name = self.menu.get_input(f"Name [{product['name']}]",
                               required=False)
    price_str = input(f"Price [{product['price_display']}]: ").strip()
    current_category = product['category']
    category = self.menu.get_input(f"Category [{current_category}]",
                                   required=False)
    stock_str = input(f"Stock [{product['stock']}]: ").strip()
    current_desc = product['description']
    description = self.menu.get_input(f"Description [{current_desc}]",
                                      required=False)

    # Build update data
    update_data = {}
    if name:
        update_data['name'] = name
    if price_str:
        try:
            update_data['price'] = float(price_str)
        except ValueError:
            self.menu.print_error("Invalid price format")
            self.menu.pause()
            return
    if category:
        update_data['category'] = category
    if stock_str:
        try:
            update_data['stock'] = int(stock_str)
        except ValueError:
            self.menu.print_error("Invalid stock format")
            self.menu.pause()
            return
    if description:
        update_data['description'] = description

    if not update_data:
        self.menu.print_info("No changes made")
        self.menu.pause()
        return

    result = self.product_controller.update_product(product_id, **update_data)

    if result['success']:
        self.menu.print_success(result['message'])
    else:
        self.menu.print_error(result['error'])

    self.menu.pause()


def _admin_delete_product(self):
    """Admin: Delete product"""
    print("\n" + "=" * 50)
    print("🗑️  DELETE PRODUCT")
    print("=" * 50)

    product_id = self.menu.get_input("Product ID to delete")

    # Check if product exists
    product_result = self.product_controller.get_product(product_id)
    if not product_result['success']:
        self.menu.print_error(product_result['error'])
        self.menu.pause()
        return

    product = product_result['product']
    product_name = product['name']
    price_display = product['price_display']
    print(f"\nProduct to delete: {product_name} - {price_display}")

    if self.menu.confirm("Are you sure you want to delete this product?"):
        result = self.product_controller.delete_product(product_id)

        if result['success']:
            self.menu.print_success(result['message'])
        else:
            self.menu.print_error(result['error'])
    else:
        self.menu.print_info("Delete cancelled")

    self.menu.pause()


def _admin_low_stock_report(self):
    """Admin: Show low stock report"""
    print("\n" + "=" * 50)
    print("📊 LOW STOCK REPORT")
    print("=" * 50)

    threshold = self.menu.get_integer_input("Stock threshold", min_val=0)

    result = self.product_controller.get_low_stock_products(threshold)

    if result['success']:
        products = result['products']

        if products:
            print(f"\n⚠️  Found {result['count']} product(s) with stock <= {threshold}")
            print(f"{'ID':<12} {'Name':<25} {'Stock':<8} {'Category':<15}")
            print("-" * 70)

            for product in products:
                print(f"{product['id']:<12} {product['name']:<25} "
                      f"{product['stock']:<8} {product['category']:<15}")
        else:
            self.menu.print_success(f"All products have stock > {threshold}")
    else:
        self.menu.print_error(result['error'])

    self.menu.pause()


def _admin_category_discount(self):
    """Admin: Apply discount to category"""
    print("\n" + "=" * 50)
    print("🏷️  APPLY CATEGORY DISCOUNT")
    print("=" * 50)

    # Get categories
    cat_result = self.product_controller.get_categories()
    if not cat_result['success']:
        self.menu.print_error(cat_result['error'])
        self.menu.pause()
        return

    categories = cat_result['categories']
    if not categories:
        self.menu.print_info("No categories available")
        self.menu.pause()
        return

    # Select category
    from src.views.menu import SimpleMenu
    category_menu = SimpleMenu("Select Category", categories)
    choice = category_menu.display()

    if choice is None:
        return

    category = categories[choice]
    discount = self.menu.get_number_input("Discount percentage", min_val=0, max_val=100)

    if self.menu.confirm(f"Apply {discount}% discount to all '{category}' products?"):
        result = self.product_controller.apply_category_discount(category, discount)

        if result['success']:
            self.menu.print_success(result['message'])
        else:
            self.menu.print_error(result['error'])
    else:
        self.menu.print_info("Discount cancelled")

    self.menu.pause()


def _admin_user_menu(self):
    """Admin user management menu"""
    from src.views.menu import SimpleMenu

    menu = SimpleMenu("User Management", [
        "👥 List All Users",
        "🔄 Change User Role",
        "🗑️  Delete User"
    ])

    choice = menu.display()
    if choice is None:
        return
    elif choice == 0:
        self._admin_list_users()
    elif choice == 1:
        self._admin_change_user_role()
    elif choice == 2:
        self._admin_delete_user()


def _admin_list_users(self):
    """Admin: List all users"""
    print("\n" + "=" * 60)
    print("👥 ALL USERS")
    print("=" * 60)

    result = self.user_controller.list_users()

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
            self.menu.print_info("No users found")
    else:
        self.menu.print_error(result['error'])

    self.menu.pause()


def _admin_change_user_role(self):
    """Admin: Change user role"""
    print("\n" + "=" * 50)
    print("🔄 CHANGE USER ROLE")
    print("=" * 50)

    user_id = self.menu.get_input("User ID")

    from src.views.menu import SimpleMenu
    role_menu = SimpleMenu("Select New Role", ["customer", "admin", "manager"])
    choice = role_menu.display()

    if choice is None:
        return

    new_role = ["customer", "admin", "manager"][choice]

    result = self.user_controller.update_user_role(user_id, new_role)

    if result['success']:
        self.menu.print_success(result['message'])
    else:
        self.menu.print_error(result['error'])

    self.menu.pause()


def _admin_delete_user(self):
    """Admin: Delete user"""
    print("\n" + "=" * 50)
    print("🗑️  DELETE USER")
    print("=" * 50)

    user_id = self.menu.get_input("User ID to delete")

    if self.menu.confirm("Are you sure you want to delete this user?"):
        result = self.user_controller.delete_user(user_id)

        if result['success']:
            self.menu.print_success(result['message'])
        else:
            self.menu.print_error(result['error'])
    else:
        self.menu.print_info("Delete cancelled")

    self.menu.pause()


def _admin_analytics(self):
    """Admin: Analytics dashboard"""
    print("\n" + "=" * 60)
    print("📊 ANALYTICS DASHBOARD")
    print("=" * 60)
    print("💡 This feature would show:")
    print("   • Sales metrics and trends")
    print("   • Popular products and categories")
    print("   • User activity statistics")
    print("   • Revenue analysis")
    print("   • Inventory insights")
    print("\n🔧 Implementation ideas:")
    print("   • Use NumPy for statistical calculations")
    print("   • Generate charts with matplotlib")
    print("   • Export reports to CSV/Excel")
    print("=" * 60)

    self.menu.pause()


def _admin_settings(self):
    """Admin: System settings"""
    print("\n" + "=" * 60)
    print("⚙️  SYSTEM SETTINGS")
    print("=" * 60)
    print("💡 This feature would include:")
    print("   • Database backup and restore")
    print("   • Data import/export utilities")
    print("   • System configuration")
    print("   • Performance monitoring")
    print("   • Log management")
    print("\n🔧 Implementation ideas:")
    print("   • CSV data import/export")
    print("   • Configuration file management")
    print("   • System health checks")
    print("=" * 60)

    self.menu.pause()


from src.views.cli_interface import WebStoreInterface

# Patch the methods into the WebStoreInterface class
def patch_admin_methods():
    """Add admin methods to WebStoreInterface class"""

    WebStoreInterface.admin_product_menu = _admin_product_menu
    WebStoreInterface.admin_add_product = _admin_add_product
    WebStoreInterface.admin_update_product = _admin_update_product
    WebStoreInterface.admin_delete_product = _admin_delete_product
    WebStoreInterface.admin_low_stock_report = _admin_low_stock_report
    WebStoreInterface.admin_category_discount = _admin_category_discount

    WebStoreInterface.admin_user_menu = _admin_user_menu
    WebStoreInterface.admin_list_users = _admin_list_users
    WebStoreInterface.admin_change_user_role = _admin_change_user_role
    WebStoreInterface.admin_delete_user = _admin_delete_user

    WebStoreInterface.admin_analytics = _admin_analytics
    WebStoreInterface.admin_settings = _admin_settings
