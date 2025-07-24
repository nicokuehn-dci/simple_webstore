"""
CSV Repository - File-based data storage using CSV format
"""
import csv
import os
from pathlib import Path
from typing import List, Dict, Optional, Any
from .repository_interface import RepositoryInterface


class CSVRepository(RepositoryInterface):
    """CSV file-based repository implementation"""
    
    def __init__(self, data_dir: str = "data"):
        """Initialize CSV repository with data directory"""
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        
        # Define CSV headers for each entity type
        self.headers = {
            'products': ['id', 'name', 'price', 'category', 'stock', 'description'],
            'users': ['id', 'username', 'email', 'role', 'created_at'],
            'cart': ['user_id', 'product_id', 'quantity', 'price']
        }
    
    def _get_file_path(self, entity_type: str) -> Path:
        """Get CSV file path for entity type"""
        return self.data_dir / f"{entity_type}.csv"
    
    def _ensure_file_exists(self, entity_type: str):
        """Ensure CSV file exists with proper headers"""
        file_path = self._get_file_path(entity_type)
        
        if not file_path.exists():
            with open(file_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                if entity_type in self.headers:
                    writer.writerow(self.headers[entity_type])
    
    def save(self, entity_type: str, data: Dict[str, Any]) -> bool:
        """Save entity data to CSV file"""
        try:
            self._ensure_file_exists(entity_type)
            file_path = self._get_file_path(entity_type)
            
            # Read existing data
            existing_data = self.load_all(entity_type)
            
            # Check if entity already exists (update) or new (append)
            entity_id = data.get('id')
            updated = False
            
            for i, row in enumerate(existing_data):
                if row.get('id') == entity_id:
                    existing_data[i] = data
                    updated = True
                    break
            
            if not updated:
                existing_data.append(data)
            
            # Write all data back to file
            with open(file_path, 'w', newline='', encoding='utf-8') as f:
                if existing_data and entity_type in self.headers:
                    writer = csv.DictWriter(f, fieldnames=self.headers[entity_type])
                    writer.writeheader()
                    writer.writerows(existing_data)
            
            return True
        except Exception as e:
            print(f"Error saving to CSV: {e}")
            return False
    
    def load_all(self, entity_type: str) -> List[Dict[str, Any]]:
        """Load all entities from CSV file"""
        try:
            file_path = self._get_file_path(entity_type)
            
            if not file_path.exists():
                return []
            
            data = []
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    # Convert numeric fields
                    if entity_type == 'products':
                        if 'price' in row:
                            row['price'] = float(row['price'])
                        if 'stock' in row:
                            row['stock'] = int(row['stock'])
                    elif entity_type == 'cart':
                        if 'quantity' in row:
                            row['quantity'] = int(row['quantity'])
                        if 'price' in row:
                            row['price'] = float(row['price'])
                    
                    data.append(row)
            
            return data
        except Exception as e:
            print(f"Error loading from CSV: {e}")
            return []
    
    def load_by_id(self, entity_type: str, entity_id: str) -> Optional[Dict[str, Any]]:
        """Load single entity by ID from CSV"""
        all_data = self.load_all(entity_type)
        
        for item in all_data:
            if item.get('id') == entity_id:
                return item
        
        return None
    
    def load_by_filter(self, entity_type: str, 
                      filters: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Load entities matching filters from CSV"""
        all_data = self.load_all(entity_type)
        results = []
        
        for item in all_data:
            match = True
            for key, value in filters.items():
                if key not in item or item[key] != value:
                    match = False
                    break
            
            if match:
                results.append(item)
        
        return results
    
    def update(self, entity_type: str, entity_id: str, 
              data: Dict[str, Any]) -> bool:
        """Update entity by ID in CSV"""
        data['id'] = entity_id
        return self.save(entity_type, data)
    
    def delete(self, entity_type: str, entity_id: str) -> bool:
        """Delete entity by ID from CSV"""
        try:
            all_data = self.load_all(entity_type)
            
            # Filter out the entity to delete
            filtered_data = [item for item in all_data if item.get('id') != entity_id]
            
            # Write filtered data back
            file_path = self._get_file_path(entity_type)
            with open(file_path, 'w', newline='', encoding='utf-8') as f:
                if filtered_data and entity_type in self.headers:
                    writer = csv.DictWriter(f, fieldnames=self.headers[entity_type])
                    writer.writeheader()
                    writer.writerows(filtered_data)
                elif entity_type in self.headers:
                    # Write just headers if no data
                    writer = csv.writer(f)
                    writer.writerow(self.headers[entity_type])
            
            return True
        except Exception as e:
            print(f"Error deleting from CSV: {e}")
            return False
    
    def exists(self, entity_type: str, entity_id: str) -> bool:
        """Check if entity exists in CSV"""
        return self.load_by_id(entity_type, entity_id) is not None
