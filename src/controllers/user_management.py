"""
User Management - Admin operations for managing users
"""
from typing import Dict
from src.services.user_service import UserService


class UserManagement:
    """Handles admin user management operations"""
    
    def __init__(self, user_service: UserService, user_auth):
        self.user_service = user_service
        self.user_auth = user_auth
    
    def list_users(self) -> Dict:
        """List all users (admin only)"""
        admin_check = self.user_auth.require_admin()
        if not admin_check['success']:
            return admin_check
        
        try:
            users = self.user_service.get_all_users()
            return {
                'success': True,
                'users': [self._format_user(u) for u in users],
                'count': len(users)
            }
        except Exception as e:
            return {'success': False, 'error': f'Failed to load users: {e}'}
    
    def update_user_role(self, user_id: str, new_role: str) -> Dict:
        """Update user role (admin only)"""
        admin_check = self.user_auth.require_admin()
        if not admin_check['success']:
            return admin_check
        
        if new_role not in ['customer', 'admin', 'manager']:
            return {'success': False, 'error': 'Invalid role'}
        
        # Check if user exists
        user = self.user_service.get_user_by_id(user_id)
        if not user:
            return {'success': False, 'error': 'User not found'}
        
        success = self.user_service.update_user_role(user_id, new_role)
        
        if success:
            return {
                'success': True,
                'message': f'Updated {user.username} role to {new_role}'
            }
        else:
            return {'success': False, 'error': 'Failed to update user role'}
    
    def delete_user(self, user_id: str) -> Dict:
        """Delete user (admin only)"""
        admin_check = self.user_auth.require_admin()
        if not admin_check['success']:
            return admin_check
        
        # Check if user exists
        user = self.user_service.get_user_by_id(user_id)
        if not user:
            return {'success': False, 'error': 'User not found'}
        
        # Prevent self-deletion
        current_user = self.user_auth.get_current_user()
        if current_user and user.id == current_user['id']:
            return {
                'success': False,
                'error': 'Cannot delete your own account'
            }
        
        success = self.user_service.delete_user(user_id)
        
        if success:
            return {
                'success': True,
                'message': f'User "{user.username}" deleted successfully'
            }
        else:
            return {'success': False, 'error': 'Failed to delete user'}
    
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
