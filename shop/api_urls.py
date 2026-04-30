from rest_framework.routers import DefaultRouter 
from . import views 
router = DefaultRouter() 
router.register('products', views.ProductViewSet) 
router.register('categories', views.CategoryViewSet) 
router.register('manufacturers', views.ManufacturerViewSet) 
router.register('carts', views.CartViewSet) 
router.register('cart-items', views.CartItemViewSet) 
urlpatterns = router.urls 
