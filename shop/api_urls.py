from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import api_views

router = DefaultRouter()
router.register(r'products', api_views.ProductViewSet, basename='product')
router.register(r'orders', api_views.OrderViewSet, basename='order')
router.register(r'categories', api_views.CategoryViewSet, basename='category')
router.register(r'manufacturers', api_views.ManufacturerViewSet, basename='manufacturer')
router.register(r'carts', api_views.CartViewSet, basename='cart')
router.register(r'cart-items', api_views.CartItemViewSet, basename='cart-item')

urlpatterns = [
    path('me/', api_views.profile_api, name='api_profile'),
    path('', include(router.urls)),
]