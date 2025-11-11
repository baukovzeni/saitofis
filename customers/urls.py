from django.urls import path
from .views import customer_list, customer_create, customer_update
app_name='customers'
urlpatterns=[path('', customer_list, name='list'), path('new/', customer_create, name='create'), path('<int:pk>/edit/', customer_update, name='update')]
