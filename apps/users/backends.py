"""
Custom authentication backends for NexusSMS.
Supports login with either username or email.
"""

from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

User = get_user_model()


class EmailOrUsernameBackend(ModelBackend):
    """
    Custom authentication backend that allows users to log in with either
    their username or email address.
    """

    def authenticate(self, request, username=None, password=None, email=None, **kwargs):
        """
        Authenticate a user by username, email, or both.
        
        Args:
            request: The HTTP request object
            username: Username or email for login
            password: User password
            email: Email address (alternative parameter)
            **kwargs: Additional keyword arguments
            
        Returns:
            User object if authentication is successful, None otherwise
        """
        # Support both 'username' parameter and 'email' parameter
        # This allows the view to pass either field name
        login_value = username or email
        
        if login_value is None or password is None:
            return None

        try:
            # Try to find user by either username or email
            user = User.objects.get(
                Q(username=login_value) | Q(email=login_value)
            )
        except User.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a nonexistent user (#20760).
            User().set_password(password)
            return None
        except User.MultipleObjectsReturned:
            # This shouldn't happen with unique constraints, but handle it
            return None

        # Check password and if the user can authenticate
        if user.check_password(password) and self.user_can_authenticate(user):
            return user

        return None

    def get_user(self, user_id):
        """
        Get a user by their ID.
        
        Args:
            user_id: The user's ID (UUID in this case)
            
        Returns:
            User object if found, None otherwise
        """
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
