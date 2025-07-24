"""
JSON Repository - Simple file-based storage using JSON
"""
import json
from pathlib import Path
from typing import List, Dict, Optional, Any

from src.repositories.repository_interface import RepositoryInterface


class JSONRepository(RepositoryInterface):
    """JSON file-based repository implementation"""
    
    def __init__(self, data_dir: str = "data"):
        """Initialize JSON repository with data directory"""
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
    
    def _get_file_path(self, entity_type: str) -> Path:
        """Get file path for entity type"""
        return self.data_dir / f"{entity_type}.json"
    
    def _load_file(self, entity_type: str) -> List[Dict[str, Any]]:
        """Load data from JSON file"""
        file_path = self._get_file_path(entity_type)
        
        if not file_path.exists():
            return []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return []
    
    def _save_file(self, entity_type: str, data: List[Dict[str, Any]]) -> bool:
        """Save data to JSON file"""
        file_path = self._get_file_path(entity_type)
        
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except IOError:
            return False
    
    def save(self, entity_type: str, data: Dict[str, Any]) -> bool:
        """Save new entity"""
        existing_data = self._load_file(entity_type)
        existing_data.append(data)
        return self._save_file(entity_type, existing_data)
    
    def load_all(self, entity_type: str) -> List[Dict[str, Any]]:
        """Load all entities of given type"""
        return self._load_file(entity_type)
    
    def load_by_id(self, entity_type: str, entity_id: str) -> Optional[Dict[str, Any]]:
        """Load single entity by ID"""
        data = self._load_file(entity_type)
        
        for item in data:
            if item.get('id') == entity_id:
                return item
        
        return None
    
    def load_by_filter(self, entity_type: str, 
                      filters: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Load entities matching filters"""
        data = self._load_file(entity_type)
        
        if not filters:
            return data
        
        filtered_data = []
        for item in data:
            matches = True
            for key, value in filters.items():
                if item.get(key) != value:
                    matches = False
                    break
            
            if matches:
                filtered_data.append(item)
        
        return filtered_data
    
    def update(self, entity_type: str, entity_id: str, 
              data: Dict[str, Any]) -> bool:
        """Update entity by ID"""
        existing_data = self._load_file(entity_type)
        
        for i, item in enumerate(existing_data):
            if item.get('id') == entity_id:
                # Update the item with new data
                existing_data[i].update(data)
                return self._save_file(entity_type, existing_data)
        
        return False
    
    def delete(self, entity_type: str, entity_id: str) -> bool:
        """Delete entity by ID"""
        existing_data = self._load_file(entity_type)
        original_length = len(existing_data)
        
        # Filter out the item to delete
        filtered_data = [item for item in existing_data 
                        if item.get('id') != entity_id]
        
        if len(filtered_data) < original_length:
            return self._save_file(entity_type, filtered_data)
        
        return False
    
    def exists(self, entity_type: str, entity_id: str) -> bool:
        """Check if entity exists"""
        return self.load_by_id(entity_type, entity_id) is not None
    
    def clear_all(self, entity_type: str) -> bool:
        """Clear all data for entity type (utility method)"""
        return self._save_file(entity_type, [])
    
    def get_count(self, entity_type: str) -> int:
        """Get count of entities (utility method)"""
        return len(self._load_file(entity_type))
