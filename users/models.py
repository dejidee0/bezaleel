import uuid
from django.core.files.storage import default_storage
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import BaseUserManager
from property.storage_backend import SupabaseStorage



class CustomUser(AbstractUser):
    """
    Custom user model extending AbstractUser.
    You can add additional fields as needed.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=150, blank=False)
    last_name = models.CharField(max_length=150, blank=False)
    email = models.EmailField(unique=True)  # Enforce unique emails
    is_verified = models.BooleanField(default=False)  # User verification status
    phone_number = models.CharField(max_length=15, blank=False, null=False)  # Optional phone number
    address = models.TextField(blank=True, null=True)  # Optional address field
    profile_picture = models.ImageField(storage=default_storage, upload_to="profiles/", blank=True, null=True)  # Stores Supabase file URL
    bio = models.TextField(blank=True, null=True)  # Optional bio field
    
    def __str__(self):
        return self.username
