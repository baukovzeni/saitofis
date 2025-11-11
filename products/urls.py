# products/urls.py
from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.product_list, name='list'),

    # API
    path('api/<int:pk>/', views.product_detail_api, name='detail_api'),
    path('api/<int:pk>/update/', views.product_update_api, name='update_api'),
    path('api/<int:pk>/image/delete/', views.product_image_delete_api, name='image_delete_api'),
    path('autocomplete/', views.product_autocomplete, name='autocomplete'),
]