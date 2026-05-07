from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models import Q

def index(request):
    return render(request, 'shop/index.html')

def about(request):
    return render(request, 'shop/about.html')

def shop_info(request):
    return render(request, 'shop/shop_info.html')

from rest_framework import viewsets, permissions
from .models import Product, Category, Manufacturer, Cart, CartItem
from .serializers import (
    ProductSerializer, CategorySerializer, 
    ManufacturerSerializer, CartSerializer, CartItemSerializer
)

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

class ManufacturerViewSet(viewsets.ModelViewSet):
    queryset = Manufacturer.objects.all()
    serializer_class = ManufacturerSerializer
    permission_classes = [permissions.IsAuthenticated]

class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]


# 🔹 Главная страница
def index(request):
    popular_products = Product.objects.all().order_by('-id')[:6]
    categories = Category.objects.all()
    return render(request, 'shop/index.html', {
        'popular_products': popular_products,
        'categories': categories,
    })

# 🔹 Статические страницы
def about(request):
    return render(request, 'shop/about.html')

def shop_info(request):
    return render(request, 'shop/shop_info.html')

# 🔹 Каталог товаров
def product_list(request):
    products = Product.objects.all()
    
    category_id = request.GET.get('category')
    if category_id:
        products = products.filter(category_id=category_id)
    
    manufacturer_id = request.GET.get('manufacturer')
    if manufacturer_id:
        products = products.filter(manufacturer_id=manufacturer_id)
    
    search = request.GET.get('search')
    if search:
        products = products.filter(Q(name__icontains=search) | Q(description__icontains=search))
    
    paginator = Paginator(products, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    categories = Category.objects.all()
    manufacturers = Manufacturer.objects.all()
    
    return render(request, 'shop/catalog.html', {
        'page_obj': page_obj,
        'categories': categories,
        'manufacturers': manufacturers,
        'current_category': category_id,
        'current_manufacturer': manufacturer_id,
        'search_query': search,
    })  # ✅ ПРАВИЛЬНО

# 🔹 Страница товара
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)  # ← ✅ Исправлено!
    return render(request, 'shop/product_detail.html', {'product': product})

# 🔹 Корзина (заглушки — реализуйте по необходимости)
def cart_view(request):
    return render(request, 'shop/cart.html')

def add_to_cart(request, product_id):
    # Ваша логика добавления
    return redirect('shop:cart_view')

def update_cart(request, item_id):
    return redirect('shop:cart_view')

def remove_from_cart(request, item_id):
    return redirect('shop:cart_view')

def checkout(request):
    return render(request, 'shop/checkout.html')