@echo off
REM Setup script for Simple WebStore (Windows)
REM This script sets up the complete environment for the webstore application

echo 🛍️  Simple WebStore Setup Script
echo ==================================

REM Check Python installation
echo 📋 Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python not found. Please install Python 3.7+
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo ✅ Python found: %PYTHON_VERSION%

REM Create directory structure
echo 📁 Creating directory structure...
if not exist "data" mkdir data
if not exist "data_csv" mkdir data_csv
if not exist "logs" mkdir logs

REM Create initial data files
echo 📊 Setting up initial data files...

REM Create sample products.json
(
echo [
echo   {
echo     "id": "p1",
echo     "name": "Laptop Pro",
echo     "price": 999.99,
echo     "category": "Electronics",
echo     "stock": 10,
echo     "description": "High-performance laptop for professionals"
echo   },
echo   {
echo     "id": "p2",
echo     "name": "Coffee Mug",
echo     "price": 12.99,
echo     "category": "Kitchen",
echo     "stock": 25,
echo     "description": "Ceramic coffee mug with ergonomic handle"
echo   },
echo   {
echo     "id": "p3",
echo     "name": "Python Book",
echo     "price": 39.99,
echo     "category": "Books",
echo     "stock": 15,
echo     "description": "Learn Python programming from basics to advanced"
echo   },
echo   {
echo     "id": "p4",
echo     "name": "Wireless Mouse",
echo     "price": 29.99,
echo     "category": "Electronics",
echo     "stock": 30,
echo     "description": "Ergonomic wireless mouse with long battery life"
echo   }
echo ]
) > data\products.json

REM Create sample users.json
(
echo [
echo   {
echo     "id": "u1",
echo     "username": "admin",
echo     "email": "admin@webstore.com",
echo     "role": "admin",
echo     "created_at": "2025-01-01T00:00:00"
echo   },
echo   {
echo     "id": "u2",
echo     "username": "customer1",
echo     "email": "customer@example.com",
echo     "role": "customer",
echo     "created_at": "2025-01-01T12:00:00"
echo   }
echo ]
) > data\users.json

REM Create empty cart.json
echo [] > data\cart.json

REM Setup CSV data
echo 📄 Setting up CSV data files...

REM Products CSV
(
echo id,name,price,category,stock,description
echo p1,Laptop Pro,999.99,Electronics,10,High-performance laptop for professionals
echo p2,Coffee Mug,12.99,Kitchen,25,Ceramic coffee mug with ergonomic handle
echo p3,Python Book,39.99,Books,15,Learn Python programming from basics to advanced
echo p4,Wireless Mouse,29.99,Electronics,30,Ergonomic wireless mouse with long battery life
) > data_csv\products.csv

REM Users CSV
(
echo id,username,email,role,created_at
echo u1,admin,admin@webstore.com,admin,2025-01-01T00:00:00
echo u2,customer1,customer@example.com,customer,2025-01-01T12:00:00
) > data_csv\users.csv

REM Cart CSV (headers only)
echo user_id,product_id,quantity,price > data_csv\cart.csv

REM Verify setup
echo 🔍 Verifying setup...

if not exist "webstore.py" (
    echo ❌ webstore.py not found
    pause
    exit /b 1
)

if not exist "webstore_csv.py" (
    echo ❌ webstore_csv.py not found
    pause
    exit /b 1
)

if not exist "src" (
    echo ❌ src directory not found
    pause
    exit /b 1
)

echo ✅ All files verified

REM Test Python imports
echo 🧪 Testing Python imports...
python -c "import sys; from pathlib import Path; sys.path.append(str(Path('.') / 'src')); from src.repositories.json_repository import JSONRepository; from src.repositories.csv_repository import CSVRepository; print('✅ All imports successful')" 2>nul
if %errorlevel% neq 0 (
    echo ❌ Import test failed
    pause
    exit /b 1
)

echo.
echo 🎉 Setup completed successfully!
echo.
echo 📚 Quick Start:
echo   JSON Storage:  python webstore.py
echo   CSV Storage:   python webstore_csv.py
echo.
echo 👤 Default Accounts:
echo   Admin:     username=admin
echo   Customer:  username=customer1
echo.
echo 📁 Data Locations:
echo   JSON files: .\data\
echo   CSV files:  .\data_csv\
echo.
echo 🛍️  Your webstore is ready to use!
echo.
pause
