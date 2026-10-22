from django.urls import path
from .views import order_cost
urlpatterns=[path('order-cost/<int:order_id>/', order_cost)]
