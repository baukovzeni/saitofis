# pos_site/urls.py
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

from django.conf import settings
from django.conf.urls.static import static
from products.views import product_list
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', product_list, name='home'),
    # auth
    path('login/',  auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # apps
    path('products/',  include(('products.urls',  'products'),  namespace='products')),
    path('customers/', include(('customers.urls', 'customers'), namespace='customers')),
    path('sales/',     include(('sales.urls',     'sales'),     namespace='sales')),
    path('reports/',   include(('reports.urls',   'reports'),   namespace='reports')),
]

# В DEV режиме раздаём /static/ и /media/ через runserver
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,  document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)