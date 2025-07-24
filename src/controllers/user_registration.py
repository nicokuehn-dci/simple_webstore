"""
User Registration - Handle new user creation
"""
from typing import Dict
from src.services.user_service import UserService


class UserRegistration:
    """Handles user registration operations"""
    
    def __init__(self, user_service: UserService):
        self.user_service = user_service
    
    def register(self, username: str, email: str, role: str = "customer") -> Dict:
        """Register a new user"""
        # Validate input
        validation = self._validate_input(username, email, role)
        if not validation['success']:
            return validation
        
        # Try to register user
        user = self.user_service.register_user(username, email, role)
        
        if user:
            return {
                'success': True,
                'user': self._format_user(user),
                'message': f'User "{username}" registered successfully'
            }
        else:
            return {'success': False, 'error': 'Username already exists'}
    
    def _validate_input(self, username: str, email: str, role: str) -> Dict:
        """Validate registration input"""
        if not username.strip():
            return {'success': False, 'error': 'Username is required'}
        
        if not email.strip() or '@' not in email:
            return {'success': False, 'error': 'Valid email is required'}
        
        if role not in ['customer', 'admin', 'manager']:
            return {'success': False, 'error': 'Invalid role'}
        
        return {'success': True}
    
    def _format_user(self, user) -> Dict:
        """Format user for display"""
        return {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role': user.role,
            'is_admin': user.is_admin,
            'display_name': f"{user.username} ({user.role})"
        }
