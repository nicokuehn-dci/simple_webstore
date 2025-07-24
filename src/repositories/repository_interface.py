"""
Repository interface - Abstract base for data storage
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Optional, Any


class RepositoryInterface(ABC):
    """Abstract repository interface for data operations"""
    
    @abstractmethod
    def save(self, entity_type: str, data: Dict[str, Any]) -> bool:
        """Save entity data to storage"""
        pass
    
    @abstractmethod
    def load_all(self, entity_type: str) -> List[Dict[str, Any]]:
        """Load all entities of given type"""
        pass
    
    @abstractmethod
    def load_by_id(self, entity_type: str, entity_id: str) -> Optional[Dict[str, Any]]:
        """Load single entity by ID"""
        pass
    
    @abstractmethod
    def load_by_filter(self, entity_type: str, 
                      filters: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Load entities matching filters"""
        pass
    
    @abstractmethod
    def update(self, entity_type: str, entity_id: str, 
              data: Dict[str, Any]) -> bool:
        """Update entity by ID"""
        pass
    
    @abstractmethod
    def delete(self, entity_type: str, entity_id: str) -> bool:
        """Delete entity by ID"""
        pass
    
    @abstractmethod
    def exists(self, entity_type: str, entity_id: str) -> bool:
        """Check if entity exists"""
        pass
