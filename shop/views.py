from django.shortcuts import render, get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Product, Cart, CartItem, Order, OrderItem
from django.core.mail import EmailMessage
from openpyxl import Workbook
from io import BytesIO
from rest_framework import viewsets, permissions
from .models import Product, Category, Manufacturer, Cart, CartItem
from .serializers import (
    ProductSerializer, CategorySerializer, 
    ManufacturerSerializer, CartSerializer, CartItemSerializer
)

def index(request):
    return render(request, 'shop/index.html')

def about(request):
    return render(request, 'shop/about.html')

def shop_info(request):
    return render(request, 'shop/shop_info.html')

def product_list(request):
    products = Product.objects.all()
    return render(request, 'shop/product_list.html', {'products': products})

def product_detail(request, pk):
    product = get_object_or_404(Product, id=pk)
    return render(request, 'shop/product_detail.html',{'product': product})

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'quantity': 1}
    )
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('shop:product_list')

def update_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    if request.method == 'POST':
        new_quantity = int(request.POST.get('quantity'))
        if new_quantity <= cart_item.product.stock:
            if new_quantity > 0:
                cart_item.quantity = new_quantity
                cart_item.save()
            else:
                cart_item.delete()
    return redirect('shop:cart_view')

def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    return redirect('shop:cart_view')

def cart_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.cartitem_set.all()
    total_price = 0
    for item in cart_items:
        total_price += item.product.price * item.quantity
    return render(request, 'shop/cart.html', {
        'cart_items': cart_items,
        'total_price': total_price
    })

@login_required
def checkout(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.cartitem_set.all()
    if not cart_items:
        return redirect('shop:product_list')
    if request.method != 'POST':
        total = sum(item.product.price * item.quantity for item in cart_items)
        return render(request, 'shop/checkout.html', {
            'cart_items': cart_items,
            'total': total
        })
    total = sum(item.product.price * item.quantity for item in cart_items)
    order = Order.objects.create(
        user=request.user,
        address=request.POST.get('address', ''),
        phone=request.POST.get('phone', ''),
        total=total
    )
    for item in cart_items:
        OrderItem.objects.create(
            order=order,
            product=item.product.name,
            quantity=item.quantity,
            price=item.product.price
        )
    wb = Workbook()
    ws = wb.active
    ws['A1'] = f'Чек заказа №{order.id}'
    ws['A2'] = f'Покупатель: {request.user.username}'
    ws['A3'] = f'Телефон: {request.POST.get("phone", "")}'
    ws['A4'] = f'Адрес: {request.POST.get("address", "")}'
    ws['A6'] = 'Товар'
    ws['B6'] = 'Кол-во'
    ws['C6'] = 'Цена'
    ws['D6'] = 'Сумма'
    
    row = 7
    for item in cart_items:
        ws[f'A{row}'] = item.product.name
        ws[f'B{row}'] = item.quantity
        ws[f'C{row}'] = float(item.product.price)
        ws[f'D{row}'] = float(item.product.price * item.quantity)
        row += 1
    
    ws[f'C{row+1}'] = 'ИТОГО:'
    ws[f'D{row+1}'] = float(total)
    
    excel_file = BytesIO()
    wb.save(excel_file)
    excel_file.seek(0)
    email = EmailMessage(
        subject=f'Чек заказа №{order.id}',
        body=f'Спасибо за покупку!\n\nВаш заказ №{order.id} на сумму {total} руб. оформлен.\nЧек во вложении.',
        from_email='shop@example.com',
        to=[request.user.email],
    )
    email.attach('receipt.xlsx', excel_file.getvalue(), 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    email.send()
    cart_items.delete()
    return render(request, 'shop/order_success.html', {'order': order})

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