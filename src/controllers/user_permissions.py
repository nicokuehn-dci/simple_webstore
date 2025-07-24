"""
User Permissions - Handle authorization checks
"""
from typing import Dict


class UserPermissions:
    """Handles user permission and authorization checks"""
    
    def __init__(self, user_auth):
        self.user_auth = user_auth
    
    def require_login(self) -> Dict:
        """Check if user is logged in"""
        if not self.user_auth.is_logged_in():
            return {'success': False, 'error': 'Please login first'}
        return {'success': True}
    
    def require_admin(self) -> Dict:
        """Check if user is admin"""
        login_check = self.require_login()
        if not login_check['success']:
            return login_check
        
        if not self.user_auth.is_admin():
            return {'success': False, 'error': 'Admin access required'}
        
        return {'success': True}
    
    def get_user_profile(self) -> Dict:
        """Get detailed profile of current user"""
        auth_check = self.require_login()
        if not auth_check['success']:
            return auth_check
        
        user = self.user_auth.current_user
        return {
            'success': True,
            'profile': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'role': user.role,
                'is_admin': user.is_admin,
                'created_at': user.created_at.isoformat() if user.created_at else None,
                'last_login': user.last_login.isoformat() if user.last_login else None
            }
        }
