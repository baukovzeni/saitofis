from django.urls import path
from .views import checkout, sale_detail
app_name='sales'
urlpatterns=[path('checkout/', checkout, name='checkout'), path('<int:pk>/', sale_detail, name='detail')]
