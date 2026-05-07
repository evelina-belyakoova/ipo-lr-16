from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from .models import Product

@api_view(['POST'])
@permission_classes([AllowAny])
def add_to_cart_api(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
 
        return Response({
            'status': 'ok',
            'message': f'{product.name} добавлен в корзину',
            'cart_count': 1 
        }, status=status.HTTP_200_OK)
        
    except Product.DoesNotExist:
        return Response({'error': 'Товар не найден'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)