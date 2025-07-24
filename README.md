# 🛍️ Simple WebStore

## � **Quick Setup & Run**

### **Option 1: Automatic Setup (Recommended)**

**Windows:**
```bash
setup.bat
```

**Linux/Mac:**
```bash
chmod +x setup.sh
./setup.sh
```

**Then run:**
```bash
# JSON storage (default)
python webstore.py

# CSV storage (Excel-compatible)
python webstore_csv.py
```

### **Option 2: Manual Setup**

1. **Install Python 3.7+** (no external dependencies needed!)
2. **Create directories:**
   ```bash
   mkdir data data_csv logs
   ```
3. **Run setup script** or manually create sample data files
4. **Start the application:**
   ```bash
   python webstore.py
   ```

## 📦 **Project Files**

### **Essential Files**
- `webstore.py` - Main application (JSON storage)
- `webstore_csv.py` - CSV version (Excel-compatible)
- `setup.sh` / `setup.bat` - Automated setup scripts
- `requirements.txt` - Dependencies (none needed!)
- `.gitignore` - Git ignore rules

### **Configuration**
- `data/` - JSON data files
- `data_csv/` - CSV data files  
- `src/` - Source code (MVC architecture)

## 👤 **Default Accounts**

After setup, you can login with:
- **Admin:** `username=admin`
- **Customer:** `username=customer1`

##  **Current Project Status: ✅ WORKING**

✅ **MVC Architecture** - Clean separation of concerns  
✅ **Dual Storage** - JSON and CSV repositories  
✅ **Modular Design** - Small, readable files (<80 lines each)  
✅ **No Dependencies** - Uses only Python standard library  
✅ **Easy Setup** - Automated setup scripts  
✅ **Sample Data** - Ready-to-use test data  

## 🎯 **Features**

- **🛒 Shopping Cart** - Add/remove products, checkout
- **👥 User Management** - Customer and admin accounts  
- **📦 Product Catalog** - Browse, search, manage inventory
- **⚙️ Admin Panel** - Product and user management
- **💾 Dual Storage** - Choose JSON or CSV format
- **🔍 Search** - Find products by name/category

## 🏗️ **Architecture**

**Clean MVC Pattern:**
```
src/
├── models/          # Data entities (Product, User, Cart)
├── repositories/    # Data storage (JSON, CSV)
├── services/        # Business logic
├── controllers/     # Request handling (split into focused components)
└── views/           # CLI interfaces (split into focused components)
```

**Split Components:**
- Controllers split into 13 focused files (auth, registration, operations, etc.)
- Views split into 10 specialized interfaces
- All files under 80 lines for maximum readability

## 📋 **Prerequisites**

- **Python 3.7+** (no additional packages required)
- **Operating System:** Windows, Linux, or macOS

## 🎮 **Usage Guide**

### **First Time Setup**
1. Run `setup.bat` (Windows) or `./setup.sh` (Linux/Mac)
2. Choose storage format: `webstore.py` (JSON) or `webstore_csv.py` (CSV)
3. Login with default accounts or register new ones

### **Customer Features**
- Browse product catalog
- Add items to shopping cart
- View cart and checkout
- Manage profile

### **Admin Features**  
- Add/edit/delete products
- Manage user accounts
- View analytics and reports
- Low stock alerts

## 📊 **Sample Data**

The setup script creates sample data including:
- **4 Products:** Laptop, Coffee Mug, Python Book, Wireless Mouse
- **2 Users:** Admin and Customer accounts
- **Categories:** Electronics, Kitchen, Books

## 🔧 **Technical Details**

### **Storage Options**
- **JSON Repository:** Human-readable, preserves types
- **CSV Repository:** Excel-compatible, smaller files

### **Data Files**
```
data/               # JSON format
├── products.json   # Product catalog
├── users.json      # User accounts  
└── cart.json       # Shopping carts

data_csv/           # CSV format  
├── products.csv    # Product catalog
├── users.csv       # User accounts
└── cart.csv        # Shopping carts
```

### **Models**
- **Product:** ID, name, price, category, stock, description
- **User:** ID, username, email, role, timestamps
- **Cart:** User cart with items and quantities

### **Business Logic**
- **Stock validation** during cart operations
- **Role-based access control** (customer/admin/manager)
- **Data validation** at service layer
- **Transaction-like operations** for checkout

## 🎓 **Learning Objectives**

This project demonstrates:
- **MVC Architecture Pattern**
- **Repository Pattern** for data abstraction
- **Clean Code Principles** (small, focused files)
- **Modular Design** with single responsibility
- **CLI Interface Design**
- **File-based Data Storage**

## 📁 **File Structure**

```
simple_webstore/
├── webstore.py                   # JSON version entry point
├── webstore_csv.py               # CSV version entry point  
├── setup.sh / setup.bat          # Setup scripts
├── requirements.txt              # Dependencies (none!)
├── .gitignore                    # Git ignore rules
├── README.md                     # This file
├── data/                         # JSON data storage
├── data_csv/                     # CSV data storage
└── src/                          # MVC Architecture
    ├── models/                   # Data entities
    │   ├── product.py            # Product model
    │   ├── user.py               # User model
    │   └── cart.py               # Cart model
    ├── repositories/             # Data access layer
    │   ├── repository_interface.py    # Abstract interface
    │   ├── json_repository.py         # JSON implementation
    │   ├── csv_repository.py          # CSV implementation
    │   └── repository_factory.py      # Factory pattern
    ├── services/                 # Business logic
    │   ├── product_service.py    # Product operations
    │   ├── user_service.py       # User management
    │   └── cart_service.py       # Cart operations
    ├── controllers/              # Request handling (13 focused files)
    │   ├── product_controller.py      # Main coordinator
    │   ├── product_operations.py      # CRUD operations
    │   ├── product_search.py          # Search functionality
    │   ├── product_management.py      # Admin management
    │   ├── user_controller.py         # Main coordinator
    │   ├── user_auth.py               # Authentication
    │   ├── user_registration.py       # Registration
    │   ├── user_management.py         # User CRUD
    │   ├── user_permissions.py        # Role management
    │   ├── cart_controller.py         # Main coordinator
    │   ├── cart_operations.py         # Cart CRUD
    │   └── cart_viewing.py            # Display/checkout
    └── views/                    # User interfaces (10 focused files)
        ├── cli_interface.py           # Main coordinator
        ├── guest_interface.py         # Guest functions
        ├── customer_interface.py      # Customer coordinator  
        ├── customer_shopping.py       # Shopping functions
        ├── customer_account.py        # Account functions
        ├── admin_product_management.py # Product admin
        ├── admin_user_management.py   # User admin
        ├── admin_reports.py           # Analytics
        └── menu.py                    # Menu utilities
```

## 🔮 **Extension Ideas**

- **Database Support:** Add MySQL/PostgreSQL repositories
- **Web Interface:** Convert CLI to web app with Flask
- **API Layer:** Add REST API endpoints
- **Order History:** Track completed orders
- **Payment Integration:** Add payment processing
- **Email Notifications:** Order confirmations
- **Advanced Search:** Filtering and sorting

## 🎯 **Educational Value**

Perfect for learning:
- **Software Architecture** patterns
- **Clean Code** principles  
- **Modular Design** concepts
- **File I/O** operations
- **CLI Application** development
- **Python OOP** concepts

## 🤝 **Contributing**

1. Fork the repository
2. Create feature branch
3. Make changes following the modular pattern
4. Keep files under 80 lines
5. Test both JSON and CSV modes
6. Submit pull request

## 📝 **License**

MIT License - Feel free to use for learning and projects.

---

**🏆 Result: Clean, modular, readable codebase that actually works!**

No scattered files, no duplicates, just proper software architecture that demonstrates MVC pattern, Repository pattern, and Clean Code principles. Exactly organized and functional! 🎉

A clean, modular e-commerce CLI application with proper MVC architecture.

## 📁 Project Structure (Clean & Organized)

```
simple_webstore/
├── src/                    # 🏗️ All source code (MVC pattern)
│   ├── models/            # Data entities
│   ├── repositories/      # Data storage layer
│   ├── services/          # Business logic
│   ├── controllers/       # Request handlers
│   └── views/             # User interfaces
├── data/                  # 💾 JSON data files
├── webstore.py           # 🚀 Main entry point
└── README.md             # 📚 This file
```

## 🚀 How to Run

```bash
python webstore.py
```

## ✨ Features That Work

✅ **Clean MVC Architecture** - Proper separation of concerns
✅ **JSON File Storage** - Persistent data storage
✅ **User Management** - Admin and customer accounts
✅ **Product Catalog** - Browse products by category
✅ **Shopping Cart** - Add/remove items, checkout
✅ **Admin Panel** - Manage products and users
✅ **CLI Interface** - Clean menu-driven interface

## 🎯 What We Have

- **Single entry point:** `webstore.py` (clean and working)
- **Organized source:** All code properly structured in `src/`
- **No duplicates:** Removed all redundant files
- **Modular design:** Each component has single responsibility
- **JSON persistence:** Data survives between sessions

## 🏆 Result

**Perfect modular structure that's readable, maintainable, and actually works!**

## 🎯 Features

- **Clean Architecture**: MVC pattern with clear separation of concerns
- **Repository Pattern**: Abstracted data storage (JSON-based)
- **User Management**: Registration, login, role-based access
- **Product Management**: CRUD operations, categories, stock tracking
- **Shopping Cart**: Add/remove items, quantity management, checkout
- **Admin Interface**: Product management, user management, analytics
- **CLI Interface**: Intuitive menu-driven interface

## 🏗️ Architecture

```
src/
├── models/              # Data entities (Product, User, Cart)
├── repositories/        # Data storage abstraction
├── services/           # Business logic layer
├── controllers/        # Request handling and validation
└── views/              # User interface (CLI)
```

## 📋 Prerequisites

- Python 3.7 or higher
- No external dependencies required (uses only standard library)

## 🚀 Quick Start

1. **Clone or download the project**
   ```bash
   cd simple_webstore
   ```

2. **Run the application**
   ```bash
   python main.py
   ```

3. **First time setup**
   - The app will create sample data automatically
   - Default admin user: `admin` / `admin@webstore.com`
   - Default customer user: `customer` / `customer@webstore.com`

## 🎮 Usage Guide

### For Customers
1. **Register** a new account or **login** with existing credentials
2. **Browse products** by category or search for specific items
3. **Add items** to your shopping cart
4. **Review cart** and proceed to **checkout**
5. View your **profile** and order history

### For Administrators
1. **Login** with admin credentials
2. Access **Product Management**:
   - Add new products
   - Update existing products
   - Delete products
   - Generate low stock reports
   - Apply bulk discounts by category
3. Access **User Management**:
   - View all users
   - Change user roles
   - Delete users
4. View **Analytics** (placeholder for future features)

## 📊 Sample Data

The application comes with sample data including:
- **Products**: Laptop, Coffee Mug, Python Book, Wireless Mouse, Notebook
- **Categories**: Electronics, Home, Books, Office
- **Users**: Admin and Customer accounts

## 🔧 Technical Details

### Models
- **Product**: ID, name, price, category, stock, description
- **User**: ID, username, email, role, timestamps
- **Cart**: User cart with items and quantities

### Data Storage
- **JSON files** in the `data/` directory
- **products.json**: All product data
- **users.json**: User accounts and profiles
- Automatic file creation and management

### Business Logic
- **Stock validation** during cart operations
- **Role-based access control** (customer/admin/manager)
- **Data validation** at service layer
- **Transaction-like operations** for checkout

## 🎓 Learning Objectives

This project demonstrates:

1. **Clean Architecture**
   - Separation of concerns
   - Dependency injection
   - Interface-based design

2. **Design Patterns**
   - Repository Pattern for data access
   - MVC (Model-View-Controller)
   - Factory Pattern (potential extension)

3. **Object-Oriented Programming**
   - Encapsulation and data validation
   - Inheritance and polymorphism (repository interface)
   - Composition over inheritance

4. **Python Best Practices**
   - Type hints for better code documentation
   - Dataclasses for clean models
   - Error handling and validation
   - Modular code organization

## 📁 File Structure

```
simple_webstore/
├── main.py                          # Application entry point
├── README.md                        # This file
├── data/                           # JSON data storage
│   ├── products.json
│   └── users.json
└── src/
    ├── models/
    │   ├── product.py              # Product entity
    │   ├── user.py                 # User entity
    │   └── cart.py                 # Cart and CartItem entities
    ├── repositories/
    │   ├── repository_interface.py  # Abstract repository
    │   └── json_repository.py      # JSON file implementation
    ├── services/
    │   ├── product_service.py      # Product business logic
    │   ├── user_service.py         # User business logic
    │   └── cart_service.py         # Cart business logic
    ├── controllers/
    │   ├── product_controller.py   # Product request handling
    │   ├── user_controller.py      # User request handling
    │   └── cart_controller.py      # Cart request handling
    └── views/
        ├── menu.py                 # CLI menu utilities
        ├── cli_interface.py        # Main CLI interface
        └── admin_interface.py      # Admin interface extensions
```

## 🔮 Extension Ideas

1. **Database Integration**
   - Create SQLRepository implementing RepositoryInterface
   - Add SQLAlchemy for ORM functionality

2. **Web Interface**
   - Flask/FastAPI web server
   - RESTful API endpoints
   - HTML templates or React frontend

3. **Advanced Features**
   - Order history and tracking
   - Product reviews and ratings
   - Inventory alerts and notifications
   - Payment processing integration

4. **Data Analysis**
   - NumPy/Pandas for sales analytics
   - Matplotlib for data visualization
   - CSV export functionality

5. **Testing**
   - Unit tests with pytest
   - Integration tests
   - Mock repositories for testing

## 🎯 Educational Value

Perfect for learning:
- **Software Architecture**: Real-world patterns and practices
- **Python Programming**: Advanced OOP concepts
- **Clean Code**: Readable, maintainable code structure
- **Project Organization**: Professional file structure
- **CLI Development**: User-friendly command-line interfaces

## 🤝 Contributing

This is an educational project. Feel free to:
- Add new features following the established patterns
- Improve error handling and validation
- Add more comprehensive documentation
- Create additional repository implementations
- Add unit tests and integration tests

## 📝 License

This project is open source and available under the MIT License.

---

*Built with ❤️ for learning clean architecture and modern Python development practices.*
