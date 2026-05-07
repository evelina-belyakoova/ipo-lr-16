
from django.contrib import admin
from django.urls import path, include
from shop import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name = 'index'),
    path('about/', views.about, name = 'about'),
    path('shop-info/', views.shop_info, name = 'shop_info'),
    path('api/', include('shop.api_urls')),
]
