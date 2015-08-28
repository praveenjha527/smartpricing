from rest_framework import viewsets
from models import Product, SuggestedPrices
from serializer import ProductSerializer, SuggestedPricesSerializer
from rest_framework import filters
from schedule import *


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class SuggestedPricesViewSet(viewsets.ModelViewSet):
    queryset = SuggestedPrices.objects.all()
    serializer_class = SuggestedPricesSerializer
    filter_backends = (filters.DjangoFilterBackend,)
