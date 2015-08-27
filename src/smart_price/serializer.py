from rest_framework import serializers
from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    seller_prices = serializers.ListField(read_only=True)
    minprice = serializers.FloatField(read_only=True)
    maxprice = serializers.FloatField(read_only=True)


    class Meta:
        model = Product