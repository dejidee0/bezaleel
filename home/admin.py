from django.contrib import admin
from .models import Property, PropertyImage

class PropertyImageInline(admin.TabularInline):  # You can use StackedInline as an alternative for stacked view
    model = PropertyImage
    extra = 1  # The number of empty forms to show initially, you can adjust this number
    max_num = 5  # Maximum number of images allowed (you can set any limit)
    fields = ['image']  # Fields you want to display in the inline

class PropertyAdmin(admin.ModelAdmin):
    inlines = [PropertyImageInline]  # Include the inline form for images in the Property form
    list_display = ('title', 'price', 'status', 'created_at')  # Adjust to your needs
    search_fields = ('title', 'address')  # Add search functionality if needed

admin.site.register(Property, PropertyAdmin)
