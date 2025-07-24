"""Admin Product Management - Product admin functions"""
from src.views.menu import SimpleMenu


def admin_product_menu(self):
    """Admin product management menu"""
    menu = SimpleMenu("📦 Product Management", [
        "➕ Add New Product",
        "✏️ Update Product",
        "🗑️ Delete Product",
        "📊 Low Stock Report",
        "💰 Category Discount"
    ])
    
    choice = menu.display()
    
    if choice == 1:
        self._admin_add_product()
    elif choice == 2:
        self._admin_update_product()
    elif choice == 3:
        self._admin_delete_product()
    elif choice == 4:
        self._admin_low_stock_report()
    elif choice == 5:
        self._admin_category_discount()


def admin_add_product(self):
    """Admin: Add new product"""
    print("\n➕ ADD NEW PRODUCT")
    print("-" * 30)
    
    name = input("Product name: ").strip()
    try:
        price = float(input("Price: €"))
        stock = int(input("Stock quantity: "))
    except ValueError:
        print("❌ Invalid price or stock quantity")
        return
    
    category = input("Category: ").strip()
    description = input("Description: ").strip()
    
    if not name or not category:
        print("❌ Name and category are required")
        return
    
    result = self.product_controller.add_product(
        name, price, category, stock, description
    )
    
    if result['success']:
        print(f"✅ {result['message']}")
    else:
        print(f"❌ {result['error']}")


def admin_update_product(self):
    """Admin: Update existing product"""
    print("\n✏️ UPDATE PRODUCT")
    print("-" * 25)
    
    # Show products first
    result = self.product_controller.list_products()
    if not result['success']:
        print(f"❌ {result['error']}")
        return
    
    products = result['products']
    if not products:
        print("No products available")
        return
    
    print("Available products:")
    for i, product in enumerate(products, 1):
        print(f"{i}. {product['name']} - €{product['price']:.2f}")
    
    try:
        choice = int(input("\nSelect product to update (number): "))
        if 1 <= choice <= len(products):
            product = products[choice - 1]
            product_id = product['id']
            
            print(f"\nUpdating: {product['name']}")
            print("(Press Enter to keep current value)")
            
            name = input(f"Name [{product['name']}]: ").strip()
            price_str = input(f"Price [{product['price']}]: €").strip()
            stock_str = input(f"Stock [{product['stock']}]: ").strip()
            category = input(f"Category [{product['category']}]: ").strip()
            description = input(f"Description [{product.get('description', '')}]: ").strip()
            
            # Use current values if empty
            name = name or product['name']
            category = category or product['category']
            description = description or product.get('description', '')
            
            try:
                price = float(price_str) if price_str else product['price']
                stock = int(stock_str) if stock_str else product['stock']
            except ValueError:
                print("❌ Invalid price or stock")
                return
            
            result = self.product_controller.update_product(
                product_id, name, price, category, stock, description
            )
            
            if result['success']:
                print(f"✅ {result['message']}")
            else:
                print(f"❌ {result['error']}")
        else:
            print("❌ Invalid selection")
    except ValueError:
        print("❌ Invalid input")
