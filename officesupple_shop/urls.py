
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from shop import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name = 'index'),
    path('about/', views.about, name = 'about'),
     path('accounts/', include('django.contrib.auth.urls')),
    path('shop-info/', views.shop_info, name = 'shop_info'),
    path('', include('shop.urls')),
    path('api/', include('shop.api_urls')),
]
