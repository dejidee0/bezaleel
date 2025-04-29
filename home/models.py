import random
import string

from django.core.files.storage import default_storage
from django.db import models
from django.conf import settings
from property.storage_backend import SupabaseStorage


def generate_property_id():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=8))


class Property(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    LABEL_CHOICES = [
        ('off_plan_houses', 'Off Plan Houses'),
        ('apartments', 'Apartments'),
        ('duplexes', 'Duplexes'),
        ('bungalows', 'Bungalows'),
        ('fully_detached_duplexes', 'Fully Detached Duplexes'),
        ('semi_detached_duplexes', 'Semi Detached Duplexes'),
        ('terrace_duplexes', 'Terrace Duplexes'),
        ('maisonettes', 'Maisonettes'),
        ('penthouses', 'Penthouses'),
        ("lands", "Lands"),
    ]

    PROPERTY_TYPE_CHOICES = [
        ('Villa', 'Villa'),
        ('Studio', 'Sudio'),
        ('Office', 'Office')
    ]

    CATEGORY_CHOICES = [
        ('off_plan_houses', 'Off Plan Houses'),
        ('apartments', 'Apartments'),
        ('duplexes', 'Duplexes'),
        ('bungalows', 'Bungalows'),
        ('fully_detached_duplexes', 'Fully Detached Duplexes'),
        ('semi_detached_duplexes', 'Semi Detached Duplexes'),
        ('terrace_duplexes', 'Terrace Duplexes'),
        ('maisonettes', 'Maisonettes'),
        ('penthouses', 'Penthouses'),
        ("lands", "Lands"),
    ]

    id = models.CharField(
        max_length=8, 
        primary_key=True, 
        unique=True, 
        editable=False, 
        default=generate_property_id
    )
    title = models.CharField(max_length=200, blank=False, null=False)
    description = models.TextField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    zip_code = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    label = models.CharField(max_length=50, choices=LABEL_CHOICES, blank=True, null=True)
    size = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)  # Size in square meters, for example
    land_area = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)  # Land area in square meters
    rooms = models.PositiveIntegerField(blank=True, null=True)
    bedrooms = models.PositiveIntegerField(blank=True, null=True)
    bathrooms = models.PositiveIntegerField(blank=True, null=True)
    year_built = models.PositiveIntegerField(blank=True, null=True)  # Year built
    video_url = models.URLField(blank=True, null=True)  # Optional video tour link
    Property_type = models.CharField(max_length=50, choices=PROPERTY_TYPE_CHOICES, default='Villa', blank=True, null=True)
    category = models.CharField(
        max_length=50, choices=CATEGORY_CHOICES, default="apartments"
    )

    price = models.CharField(max_length=50, blank=True, null=True)
    agent = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='properties'
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='approved', blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title if self.title else "Untitled Property"
    
    
class PropertyImage(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(storage=default_storage, upload_to="properties/") # Stores Supabase file URL
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.property.title if self.property.title else 'Unknown Property'}"
