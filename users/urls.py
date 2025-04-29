from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Your other URL patterns
    
    # Login URL
    path('login/', views.custom_login_view, name='login'),
    
    # Logout URL
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    # Register URL
    path('register/', views.register, name='register'),
]