from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='home'),

    path('dashboard/', dashboard, name='dashboard'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
    path('faq/', faq, name='faq'),
    path('services/', services, name='services'),
    path('add-property/', add_property, name='add_property'),
    # path('verification-required/', verification_required, name='verification_required'),
    path('my-profile/', my_profile, name='my_profile'),
    path('direct-contact/', direct_contact, name='direct_contact'),
    path('property-detail/<str:property_id>/', property_detail, name='property_detail'),
    path('properties/', all_properties, name='all_properties'),
    path('category/<str:category>/', category_properties, name='category'),

]