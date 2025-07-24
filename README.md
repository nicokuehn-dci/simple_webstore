# 🛍️ Simple WebStore

A clean, modular CLI e-commerce application demonstrating MVC architecture with dual storage support.

## 🚀 Quick Start

### Windows

```bash
setup.bat
python webstore.py
```

### Linux/Mac

```bash
chmod +x setup.sh && ./setup.sh
python webstore.py
```

### Storage Options

- `python webstore.py` - JSON storage (default)
- `python webstore_csv.py` - CSV storage (Excel-compatible)

## ✨ Features

- 🛒 **Shopping Cart** - Add/remove products, checkout
- 👥 **User Management** - Customer and admin accounts
- 📦 **Product Catalog** - Browse, search, manage inventory
- ⚙️ **Admin Panel** - Product and user management
- 💾 **Dual Storage** - JSON or CSV format
- 🔍 **Search** - Find products by name/category
- 🌐 **Cross-Platform** - Windows, Linux, macOS

## 🏗️ Architecture

Clean MVC Pattern:

```text
src/
├── models/          # Data entities (Product, User, Cart)
├── repositories/    # Data storage (JSON, CSV)
├── services/        # Business logic
├── controllers/     # Request handling
└── views/           # CLI interfaces
```

## 📋 Prerequisites

- **Python 3.7+** (no external dependencies!)
- **Any OS:** Windows, Linux, or macOS

## 👤 Default Accounts

- **Admin:** `username=admin`
- **Customer:** `username=customer1`

## 🎯 Technical Features

✅ **MVC Architecture** - Clean separation of concerns  
✅ **Repository Pattern** - Abstracted data storage  
✅ **Zero Dependencies** - Pure Python standard library  
✅ **Modular Design** - Focused, readable components  
✅ **Cross-Platform** - Works everywhere Python runs

## 📁 File Structure

```text
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
    ├── repositories/             # Data access layer
    ├── services/                 # Business logic
    ├── controllers/              # Request handling
    └── views/                    # User interfaces
```

## 🔮 Extension Ideas

- **Database Support:** Add MySQL/PostgreSQL repositories
- **Web Interface:** Convert CLI to web app with Flask
- **API Layer:** Add REST API endpoints
- **Order History:** Track completed orders
- **Payment Integration:** Add payment processing

## 🎓 Educational Value

Perfect for learning:

- **Software Architecture** patterns
- **Clean Code** principles  
- **Modular Design** concepts
- **File I/O** operations
- **CLI Application** development
- **Python OOP** concepts

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Make changes following the modular pattern
4. Keep files under 80 lines
5. Test both JSON and CSV modes
6. Submit pull request

## 📝 License

MIT License - Feel free to use for learning and projects.

---

**🏆 A clean, modular e-commerce CLI demonstrating professional software architecture!**
