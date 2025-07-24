#!/bin/bash
# Setup script for Simple WebStore
# This script sets up the complete environment for the webstore application

echo "🛍️  Simple WebStore Setup Script"
echo "=================================="

# Check Python version
echo "📋 Checking Python installation..."
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
    echo "✅ Python3 found: $(python3 --version)"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
    python_version=$(python --version 2>&1)
    if [[ $python_version == *"Python 3"* ]]; then
        echo "✅ Python found: $python_version"
    else
        echo "❌ Python 3.7+ required. Found: $python_version"
        exit 1
    fi
else
    echo "❌ Python not found. Please install Python 3.7+"
    exit 1
fi

# Create directory structure
echo "📁 Creating directory structure..."
mkdir -p data
mkdir -p data_csv
mkdir -p logs

# Create initial data files
echo "📊 Setting up initial data files..."

# Create sample products.json
cat > data/products.json << 'EOF'
[
  {
    "id": "p1",
    "name": "Laptop Pro",
    "price": 999.99,
    "category": "Electronics",
    "stock": 10,
    "description": "High-performance laptop for professionals"
  },
  {
    "id": "p2",
    "name": "Coffee Mug",
    "price": 12.99,
    "category": "Kitchen",
    "stock": 25,
    "description": "Ceramic coffee mug with ergonomic handle"
  },
  {
    "id": "p3",
    "name": "Python Book",
    "price": 39.99,
    "category": "Books",
    "stock": 15,
    "description": "Learn Python programming from basics to advanced"
  },
  {
    "id": "p4",
    "name": "Wireless Mouse",
    "price": 29.99,
    "category": "Electronics",
    "stock": 30,
    "description": "Ergonomic wireless mouse with long battery life"
  }
]
EOF

# Create sample users.json with admin account
cat > data/users.json << 'EOF'
[
  {
    "id": "u1",
    "username": "admin",
    "email": "admin@webstore.com",
    "role": "admin",
    "created_at": "2025-01-01T00:00:00"
  },
  {
    "id": "u2",
    "username": "customer1",
    "email": "customer@example.com",
    "role": "customer",
    "created_at": "2025-01-01T12:00:00"
  }
]
EOF

# Create empty cart.json
echo "[]" > data/cart.json

# Setup CSV data (copy from JSON)
echo "📄 Setting up CSV data files..."

# Products CSV
cat > data_csv/products.csv << 'EOF'
id,name,price,category,stock,description
p1,Laptop Pro,999.99,Electronics,10,High-performance laptop for professionals
p2,Coffee Mug,12.99,Kitchen,25,Ceramic coffee mug with ergonomic handle
p3,Python Book,39.99,Books,15,Learn Python programming from basics to advanced
p4,Wireless Mouse,29.99,Electronics,30,Ergonomic wireless mouse with long battery life
EOF

# Users CSV
cat > data_csv/users.csv << 'EOF'
id,username,email,role,created_at
u1,admin,admin@webstore.com,admin,2025-01-01T00:00:00
u2,customer1,customer@example.com,customer,2025-01-01T12:00:00
EOF

# Cart CSV (empty with headers)
cat > data_csv/cart.csv << 'EOF'
user_id,product_id,quantity,price
EOF

# Set proper permissions
echo "🔐 Setting file permissions..."
chmod 644 data/*.json
chmod 644 data_csv/*.csv
chmod +x webstore.py
chmod +x webstore_csv.py

# Verify setup
echo "🔍 Verifying setup..."

# Check if main files exist
if [[ -f "webstore.py" && -f "webstore_csv.py" ]]; then
    echo "✅ Main application files found"
else
    echo "❌ Main application files missing"
    exit 1
fi

# Check if src directory exists
if [[ -d "src" ]]; then
    echo "✅ Source directory structure found"
else
    echo "❌ Source directory missing"
    exit 1
fi

# Test Python import
echo "🧪 Testing Python imports..."
$PYTHON_CMD -c "
import sys
from pathlib import Path
sys.path.append(str(Path('.') / 'src'))
try:
    from src.repositories.json_repository import JSONRepository
    from src.repositories.csv_repository import CSVRepository
    print('✅ All imports successful')
except ImportError as e:
    print(f'❌ Import error: {e}')
    exit(1)
" || exit 1

echo ""
echo "🎉 Setup completed successfully!"
echo ""
echo "📚 Quick Start:"
echo "  JSON Storage:  $PYTHON_CMD webstore.py"
echo "  CSV Storage:   $PYTHON_CMD webstore_csv.py"
echo ""
echo "👤 Default Accounts:"
echo "  Admin:     username=admin"
echo "  Customer:  username=customer1"
echo ""
echo "📁 Data Locations:"
echo "  JSON files: ./data/"
echo "  CSV files:  ./data_csv/"
echo ""
echo "🛍️  Your webstore is ready to use!"
