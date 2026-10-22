from django.urls import path
from . import views
urlpatterns=[path('summary/',views.financial_summary,name='financial-summary'),path('invoice/<int:order_id>/',views.invoice,name='invoice')]
