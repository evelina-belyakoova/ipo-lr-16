<<<<<<< HEAD
from django.urls import path
from . import api_views

urlpatterns = [
    path('cart/add/<int:product_id>/', api_views.add_to_cart_api, name='add_to_cart_api'),
]
=======
from rest_framework.routers import DefaultRouter 
from . import views 
router = DefaultRouter() 
router.register('products', views.ProductViewSet) 
router.register('categories', views.CategoryViewSet) 
router.register('manufacturers', views.ManufacturerViewSet) 
router.register('carts', views.CartViewSet) 
router.register('cart-items', views.CartItemViewSet) 
urlpatterns = router.urls 
>>>>>>> 408cd0cbc27aea19f09c977846944577d1091599
