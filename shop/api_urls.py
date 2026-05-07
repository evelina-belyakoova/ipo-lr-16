from django.urls import path
from . import api_views

urlpatterns = [
    path('cart/add/<int:product_id>/', api_views.add_to_cart_api, name='add_to_cart_api'),
]