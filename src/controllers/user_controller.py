"""
User Controller - Main coordinator for user operations
"""
from typing import Dict, Optional
from src.services.user_service import UserService
from .user_auth import UserAuth
from .user_registration import UserRegistration
from .user_management import UserManagement
from .user_permissions import UserPermissions


class UserController:
    """Main controller that coordinates all user operations"""
    
    def __init__(self, user_service: UserService):
        """Initialize controller with all user components"""
        self.user_service = user_service
        
        # Initialize components
        self.auth = UserAuth(user_service)
        self.registration = UserRegistration(user_service)
        self.permissions = UserPermissions(self.auth)
        self.management = UserManagement(user_service, self.permissions)
    
    # Auth operations
    def login(self, username: str, password: Optional[str] = None) -> Dict:
        return self.auth.login(username, password)
    
    def logout(self) -> Dict:
        return self.auth.logout()
    
    def get_current_user(self) -> Optional[Dict]:
        return self.auth.get_current_user()
    
    def is_logged_in(self) -> bool:
        return self.auth.is_logged_in()
    
    def is_admin(self) -> bool:
        return self.auth.is_admin()
    
    # Registration operations
    def register(self, username: str, email: str,
                 password: Optional[str] = None,
                 role: str = "customer") -> Dict:
        # For now, ignore password in registration (store in demo_passwords)
        _ = password  # Acknowledge the parameter
        return self.registration.register(username, email, role)
    
    # Permission operations
    def require_login(self) -> Dict:
        return self.permissions.require_login()
    
    def require_admin(self) -> Dict:
        return self.permissions.require_admin()
    
    def get_user_profile(self) -> Dict:
        return self.permissions.get_user_profile()
    
    # Management operations (admin only)
    def list_users(self) -> Dict:
        return self.management.list_users()
    
    def update_user_role(self, user_id: str, new_role: str) -> Dict:
        return self.management.update_user_role(user_id, new_role)
    
    def delete_user(self, user_id: str) -> Dict:
        return self.management.delete_user(user_id)
