from rest_framework import viewsets

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from .models import Category, Product, Order
from .serializers import (
    CategorySerializer,
    ProductSerializer,
    OrderSerializer,
)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.order_by("id")
    serializer_class = CategorySerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.select_related("category").order_by("id")
    serializer_class = ProductSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.order_by("id")
    serializer_class = OrderSerializer

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


## cf7c58738a8f2d44d3fe8a33618a7ce5a5dff188
## CharlieBrownJr!@#
