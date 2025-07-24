"""
User model - Simple user entity with role-based access
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class User:
    """Simple user entity with role validation"""
    id: str
    username: str
    email: str
    role: str = "customer"  # customer, admin, manager
    created_at: Optional[datetime] = None
    last_login: Optional[datetime] = None
    
    def __post_init__(self):
        """Validate user data after initialization"""
        if self.created_at is None:
            self.created_at = datetime.now()
        
        # Basic validation
        if not self.username.strip():
            raise ValueError("Username cannot be empty")
        if not self.email or '@' not in self.email:
            raise ValueError("Invalid email address")
        if self.role not in ['customer', 'admin', 'manager']:
            raise ValueError("Invalid user role")
    
    @property
    def is_admin(self) -> bool:
        """Check if user has admin privileges"""
        return self.role in ['admin', 'manager']
    
    def to_dict(self) -> dict:
        """Convert user to dictionary for storage"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'role': self.role,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'User':
        """Create user from dictionary"""
        # Handle datetime conversions
        created_at = None
        last_login = None
        
        if data.get('created_at'):
            created_at = datetime.fromisoformat(data['created_at'])
        if data.get('last_login'):
            last_login = datetime.fromisoformat(data['last_login'])
        
        return cls(
            id=data['id'],
            username=data['username'],
            email=data['email'],
            role=data.get('role', 'customer'),
            created_at=created_at,
            last_login=last_login
        )
    
    def update_last_login(self) -> 'User':
        """Return new user with updated last login"""
        return User(
            id=self.id,
            username=self.username,
            email=self.email,
            role=self.role,
            created_at=self.created_at,
            last_login=datetime.now()
        )
    
    def change_role(self, new_role: str) -> 'User':
        """Return new user with updated role"""
        if new_role not in ['customer', 'admin', 'manager']:
            raise ValueError("Invalid user role")
        
        return User(
            id=self.id,
            username=self.username,
            email=self.email,
            role=new_role,
            created_at=self.created_at,
            last_login=self.last_login
        )
    
    def __str__(self) -> str:
        """String representation for display"""
        admin_badge = " 👑" if self.is_admin else ""
        return f"{self.username} ({self.role}){admin_badge} - {self.email}"
