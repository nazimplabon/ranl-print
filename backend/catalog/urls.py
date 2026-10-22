from django.urls import path
from . import views
urlpatterns = [path('catalog/products/', views.products, name='catalog-products'), path('catalog/calculate/', views.calculate, name='catalog-calculate')]
