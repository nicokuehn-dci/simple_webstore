"""
User Authentication - Login/Logout functionality
"""
from typing import Dict, Optional
from src.services.user_service import UserService


class UserAuth:
    """Handles user authentication operations"""
    
    def __init__(self, user_service: UserService):
        self.user_service = user_service
        self.current_user = None
    
    def login(self, username: str) -> Dict:
        """Login user by username"""
        if not username.strip():
            return {'success': False, 'error': 'Username is required'}
        
        user = self.user_service.authenticate_user(username)
        
        if user:
            self.current_user = user
            return {
                'success': True,
                'user': self._format_user(user),
                'message': f'Welcome back, {user.username}!',
                'is_admin': user.is_admin
            }
        else:
            return {'success': False, 'error': 'User not found'}
    
    def logout(self) -> Dict:
        """Logout current user"""
        if self.current_user:
            username = self.current_user.username
            self.current_user = None
            return {
                'success': True,
                'message': f'Goodbye, {username}!'
            }
        else:
            return {'success': False, 'error': 'No user logged in'}
    
    def get_current_user(self) -> Optional[Dict]:
        """Get current logged-in user"""
        if self.current_user:
            return self._format_user(self.current_user)
        return None
    
    def is_logged_in(self) -> bool:
        """Check if user is logged in"""
        return self.current_user is not None
    
    def is_admin(self) -> bool:
        """Check if current user is admin"""
        return self.current_user and self.current_user.is_admin
    
    def _format_user(self, user, detailed: bool = False) -> Dict:
        """Format user for display"""
        basic_info = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role': user.role,
            'is_admin': user.is_admin,
            'display_name': f"{user.username} ({user.role})"
        }
        
        if detailed:
            basic_info.update({
                'created_at': user.created_at.isoformat() if user.created_at else None,
                'last_login': user.last_login.isoformat() if user.last_login else None
            })
        
        return basic_info
