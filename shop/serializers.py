from rest_framework import serializers
from .models import Product, Category, Manufacturer, Cart, CartItem, Profile, Order, OrderItem


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ManufacturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manufacturer
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['id', 'user', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']


class CartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    item_total = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['id', 'cart', 'product', 'product_name', 'quantity', 'item_total']
        read_only_fields = ['id', 'cart']

    def get_item_total(self, obj):
        return obj.product.price * obj.quantity

class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', required=False)
    favorite_category_name = serializers.CharField(
        source='favorite_category.name', 
        read_only=True, 
        default='—'
    )
    
    class Meta:
        model = Profile
        fields = [
            'id', 'username', 'email', 'role', 
            'phone', 'address', 
            'favorite_category', 'favorite_category_name',
            'delivery_city', 'postal_code'
        ]
        read_only_fields = ['id', 'username', 'role']
    
    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)
        if user_data:
            user = instance.user
            user.email = user_data.get('email', user.email)
            user.save()
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'price']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'address', 'phone', 'total', 'created_at', 'items']
        read_only_fields = ['id', 'user', 'created_at', 'total']