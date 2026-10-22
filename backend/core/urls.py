from django.urls import path
from . import views

urlpatterns = [
    path('csrf/', views.csrf, name='api-csrf'),
    path('contact/', views.create_contact, name='contact-create'),
]
