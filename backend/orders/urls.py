from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.order_list, name='orders-list'),
    path('track/', views.track_order, name='orders-track'),
]
