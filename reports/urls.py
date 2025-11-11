# reports/urls.py
from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('daily/', views.report_daily, name='daily'),
    path('sale/bulk/delete/', views.sale_delete_bulk, name='sale_delete_bulk'),
]