from django.urls import path
from . import views
urlpatterns = [path('quotes/create/', views.create_quote, name='quote-create')]
