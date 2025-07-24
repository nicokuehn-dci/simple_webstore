# 📁 Repository Options

## Available Storage Types

Your webstore now supports **TWO storage formats**:

### 1. **JSON Repository** (Default)
- **Files**: `data/products.json`, `data/users.json`, `data/cart.json`
- **Format**: Human-readable JSON
- **Usage**: `python webstore.py`

### 2. **CSV Repository** (New!)
- **Files**: `data_csv/products.csv`, `data_csv/users.csv`, `data_csv/cart.csv`
- **Format**: Excel-compatible CSV
- **Usage**: `python webstore_csv.py`

## File Formats

### JSON Format (products.json)
```json
[
  {
    "id": "p1",
    "name": "Laptop Pro",
    "price": 999.99,
    "category": "Electronics",
    "stock": 10,
    "description": "High-performance laptop"
  }
]
```

### CSV Format (products.csv)
```csv
id,name,price,category,stock,description
p1,Laptop Pro,999.99,Electronics,10,High-performance laptop
p2,Coffee Mug,12.99,Kitchen,25,Ceramic coffee mug
```

## Benefits

**JSON Repository:**
✅ Human-readable  
✅ Preserves data types  
✅ Easy to edit manually  
✅ Supports nested structures  

**CSV Repository:**
✅ Excel-compatible  
✅ Smaller file sizes  
✅ Easy data import/export  
✅ Database-friendly format  

## Quick Switch

```bash
# Use JSON storage (default)
python webstore.py

# Use CSV storage  
python webstore_csv.py
```

**Both repositories implement the same interface, so all features work identically!** 🎯
