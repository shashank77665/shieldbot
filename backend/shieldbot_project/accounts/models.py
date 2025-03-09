from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class ShieldbotUser(AbstractUser):
    """
    Custom user model that extends Django's built-in AbstractUser.
    Includes all standard fields from AbstractUser (username, email, password, is_superuser, etc.)
    plus some custom fields.
    """
    profile_picture = models.ImageField(upload_to='profile_pics/', default='user.jpg')
    # created_at is replaced by date_joined from AbstractUser
    
    class Meta:
        verbose_name = 'Shieldbot User'
        verbose_name_plural = 'Shieldbot Users'
    
    def __str__(self):
        return f"{self.username}"
    
    @property
    def shieldbot_user_id(self):
        """Alias for the primary key, used in JWT creation and elsewhere."""
        return self.id
    
    @staticmethod
    def validate_fields(data):
        """Validate and truncate fields to conform to database constraints."""
        data["username"] = data.get("username", "")[:50]
        data["email"] = data.get("email", "")[:100]
        return data

# Create an alias so that 'User' can be imported in other modules
User = ShieldbotUser 