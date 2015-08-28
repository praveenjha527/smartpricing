from rest_framework import serializers
from .models import Product, Store, SuggestedPrices


class ProductSerializer(serializers.ModelSerializer):
    seller_prices = serializers.ListField(read_only=True)
    min_online_price = serializers.FloatField(read_only=True)
    max_online_price = serializers.FloatField(read_only=True)
    brand = serializers.SlugRelatedField(slug_field='name', read_only=True)
    category = serializers.SlugRelatedField(slug_field='category_id', read_only=True)
    region = serializers.SlugRelatedField(slug_field='region_id', read_only=True)

    class Meta:
        model = Product
        fields = ('product_id', 'seller_prices', 'min_online_price', 'min_online_price', 'brand', 'category')


class StoreSerializer(serializers.ModelSerializer):
    region = serializers.SlugRelatedField(slug_field='region_id', read_only=True)

    class Meta:
        model = Store
        fields = ('store_id',)


class SuggestedPricesSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    store = StoreSerializer(read_only=True)
    region_id = serializers.SerializerMethodField()

    class Meta:
        model = SuggestedPrices
        fields = ('product', 'store', 'region_id', 'suggested_price')

    def get_region(self, obj):
        return obj.product.region.region_id