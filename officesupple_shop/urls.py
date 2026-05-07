from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from shop import views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('shop-info/', views.shop_info, name='shop_info'),
    
    path('accounts/', include('django.contrib.auth.urls')),
    

    path('', include('shop.urls')),
<<<<<<< HEAD
    
    path('api/', include('shop.api_urls')),

=======
    path('api/', include('shop.api_urls')),
>>>>>>> 408cd0cbc27aea19f09c977846944577d1091599
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)