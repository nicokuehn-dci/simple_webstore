"""
Setup Verification - Check if webstore is properly configured
"""
import sys
from pathlib import Path
import os

def verify_setup():
    print("🔍 Simple WebStore Setup Verification")
    print("=" * 50)
    
    # Check Python version
    python_version = sys.version_info
    print(f"🐍 Python Version: {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    if python_version.major >= 3 and python_version.minor >= 7:
        print("✅ Python version compatible")
    else:
        print("❌ Python 3.7+ required")
        return False
    
    # Check directories
    dirs = ["data", "data_csv", "logs", "src"]
    for dir_name in dirs:
        if os.path.exists(dir_name):
            print(f"✅ Directory exists: {dir_name}/")
        else:
            print(f"❌ Missing directory: {dir_name}/")
            return False
    
    # Check main files
    files = ["webstore.py", "webstore_csv.py", "requirements.txt", ".gitignore"]
    for file_name in files:
        if os.path.exists(file_name):
            print(f"✅ File exists: {file_name}")
        else:
            print(f"❌ Missing file: {file_name}")
    
    # Check data files
    json_files = ["data/products.json", "data/users.json", "data/cart.json"]
    csv_files = ["data_csv/products.csv", "data_csv/users.csv", "data_csv/cart.csv"]
    
    for file_name in json_files + csv_files:
        if os.path.exists(file_name):
            print(f"✅ Data file: {file_name}")
        else:
            print(f"⚠️  Missing data file: {file_name}")
    
    # Test imports
    try:
        sys.path.append(str(Path('.') / 'src'))
        from src.repositories.json_repository import JSONRepository
        from src.repositories.csv_repository import CSVRepository
        print("✅ All imports working")
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    
    # Test repositories
    try:
        json_repo = JSONRepository("data")
        csv_repo = CSVRepository("data_csv")
        
        json_products = json_repo.load_all("products")
        csv_products = csv_repo.load_all("products")
        
        print(f"✅ JSON Repository: {len(json_products)} products")
        print(f"✅ CSV Repository: {len(csv_products)} products")
    except Exception as e:
        print(f"⚠️  Repository test failed: {e}")
    
    print("\n🎉 Setup verification completed!")
    print("\n📚 Ready to run:")
    print("   python webstore.py      # JSON storage")
    print("   python webstore_csv.py  # CSV storage")
    print("\n👤 Default accounts:")
    print("   admin / customer1")
    
    return True

if __name__ == "__main__":
    verify_setup()
