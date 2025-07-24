"""Admin Reports - Analytics and reporting functions"""


def admin_analytics(interface):
    """Admin: Show analytics dashboard"""
    print("\n" + "=" * 50)
    print("📊 ANALYTICS DASHBOARD")
    print("=" * 50)
    
    # Product statistics
    product_result = interface.product_controller.list_products()
    if product_result['success']:
        products = product_result['products']
        total_products = len(products)
        total_stock = sum(p['stock'] for p in products)
        avg_price = sum(p['price'] for p in products) / total_products if products else 0
        
        print(f"📦 Products: {total_products}")
        print(f"📋 Total Stock: {total_stock}")
        print(f"💰 Average Price: €{avg_price:.2f}")
    
    # User statistics
    user_result = interface.user_controller.list_users()
    if user_result['success']:
        users = user_result['users']
        total_users = len(users)
        admin_count = sum(1 for u in users if u['role'] == 'admin')
        customer_count = sum(1 for u in users if u['role'] == 'customer')
        
        print(f"👥 Total Users: {total_users}")
        print(f"🔑 Admins: {admin_count}")
        print(f"🛒 Customers: {customer_count}")
    
    print("=" * 50)
    input("Press Enter to continue...")


def admin_low_stock_report(interface):
    """Admin: Show low stock report"""
    print("\n📊 LOW STOCK REPORT")
    print("-" * 30)
    
    threshold = 5  # Low stock threshold
    
    result = interface.product_controller.list_products()
    
    if result['success']:
        products = result['products']
        low_stock = [p for p in products if p['stock'] <= threshold]
        
        if low_stock:
            print(f"⚠️ Found {len(low_stock)} products with low stock:")
            print()
            
            for product in low_stock:
                print(f"📦 {product['name']}")
                print(f"   Stock: {product['stock']} (⚠️ Low)")
                print(f"   Category: {product['category']}")
                print()
        else:
            print("✅ All products have sufficient stock")
    else:
        print(f"❌ {result['error']}")
    
    input("Press Enter to continue...")


def admin_settings(interface):
    """Admin: Application settings"""
    print("\n⚙️ SYSTEM SETTINGS")
    print("-" * 25)
    print("🔧 Configuration options:")
    print("• Data storage: JSON files")
    print("• User roles: customer, admin, manager")
    print("• Stock threshold: 5 items")
    print("• Currency: Euro (€)")
    print()
    print("✅ System running normally")
    input("Press Enter to continue...")
