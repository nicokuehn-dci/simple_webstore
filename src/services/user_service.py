"""
User Service - Business logic for user operations
"""
from typing import Optional
import uuid

from src.models.user import User


class UserService:
    """Service for user-related business operations"""

    def __init__(self, repository):
        """Initialize service with repository"""
        self.repository = repository

    def register_user(self, username: str, email: str,
                      role: str = "customer") -> Optional[User]:
        """Register a new user"""
        # Check if username already exists
        existing_users = self.repository.load_by_filter('users',
                                                       {'username': username})
        if existing_users:
            return None

        try:
            # Generate unique ID
            user_id = self._generate_user_id()

            # Create user instance (validates data)
            user = User(
                id=user_id,
                username=username,
                email=email,
                role=role
            )

            # Save to repository
            if self.repository.save('users', user.to_dict()):
                return user
            return None

        except ValueError as e:
            print(f"Error creating user: {e}")
            return None

    def authenticate_user(self, username: str) -> Optional[User]:
        """Simple authentication by username"""
        users = self.repository.load_by_filter('users', {'username': username})
        if users:
            user = User.from_dict(users[0])
            # Update last login
            updated_user = user.update_last_login()
            self.repository.update('users', user.id,
                                 {'last_login': updated_user.last_login.isoformat()})
            return updated_user
        return None

    def get_user_by_id(self, user_id: str) -> Optional[User]:
        """Get user by ID"""
        data = self.repository.load_by_id('users', user_id)
        return User.from_dict(data) if data else None

    def get_user_by_username(self, username: str) -> Optional[User]:
        """Get user by username"""
        users = self.repository.load_by_filter('users', {'username': username})
        return User.from_dict(users[0]) if users else None

    def get_all_users(self) -> list[User]:
        """Get all users (admin function)"""
        data = self.repository.load_all('users')
        return [User.from_dict(item) for item in data]

    def update_user_role(self, user_id: str, new_role: str) -> bool:
        """Update user role (admin function)"""
        if new_role not in ['customer', 'admin', 'manager']:
            return False

        return self.repository.update('users', user_id, {'role': new_role})

    def delete_user(self, user_id: str) -> bool:
        """Delete a user (admin function)"""
        return self.repository.delete('users', user_id)

    def get_users_by_role(self, role: str) -> list[User]:
        """Get users by role"""
        data = self.repository.load_by_filter('users', {'role': role})
        return [User.from_dict(item) for item in data]

    def _generate_user_id(self) -> str:
        """Generate unique user ID"""
        while True:
            # Use UUID for uniqueness
            user_id = f"USR-{str(uuid.uuid4())[:8].upper()}"

            # Check if ID already exists
            if not self.repository.exists('users', user_id):
                return user_id
