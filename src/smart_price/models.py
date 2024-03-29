import requests
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType

PRICES_HOST = "http://45.56.112.85"

CRAWLED_HOST = "http://128.199.238.212/"
CRAWLED_URN = "product/minprice/{product_id}/"


class DiscountRule(models.Model):
    name = models.CharField(max_length=255)
    value = models.IntegerField()
    discount_op = models.CharField(max_length=1, choices=(
        ('-', 'Flat'),
        ('%', 'Percentage')))

    def __unicode__(self):
        return u'{0}'.format(self.name)


class VariationRule(models.Model):
    rule_name = models.CharField(max_length=255)
    rule_operator = models.CharField(max_length=1)

    def __unicode__(self):
        return u'{0}'.format(self.rule_name)

class VariationFactor(models.Model):
    name = models.CharField(max_length=255)
    factor_value = models.FloatField()
    factor_types = models.ForeignKey(VariationRule, related_name='factors')
    # rule_weight = models.IntegerField(null=True)
    limit = models.Q(app_label = 'smart_price', model = 'product')\
            | models.Q(app_label = 'smart_price', model = 'brand')\
            | models.Q(app_label = 'smart_price', model = 'region')\
            | models.Q(app_label = 'smart_price', model = 'category')
    content_type = models.ForeignKey(ContentType, limit_choices_to=limit)
    object_id = models.PositiveIntegerField()
    factor_target = GenericForeignKey('content_type', 'object_id')
    variation_discount = models.ForeignKey(DiscountRule)

    def __unicode__(self):
        return u'{0}'.format(self.name)


class Brand(models.Model):
    name = models.CharField(max_length=255)
    variation_factors = GenericRelation(VariationFactor, related_query_name='variation_factors')

    def __unicode__(self):
        return u'{0}'.format(self.name)


class Category(models.Model):
    category_id = models.IntegerField()
    variation_factors = GenericRelation(VariationFactor, related_query_name='variation_factors')

    def __unicode__(self):
        return u'{0}'.format(self.category_id)


class Region(models.Model):
    region_id = models.IntegerField()
    variation_factors = GenericRelation(VariationFactor, related_query_name='variation_factors')

    def __unicode__(self):
        return u'{0}'.format(self.region_id)


class Product(models.Model):
    product_id = models.IntegerField()
    brand = models.ForeignKey(Brand, related_name='products')
    category = models.ForeignKey(Category, related_name='products')
    region = models.ForeignKey(Region, related_name='products')
    variation_factors = GenericRelation(VariationFactor, related_query_name='variation_factors')

    def __unicode__(self):
        return u'{0}'.format(self.product_id)

    class Meta:
        unique_together = (('product_id', 'brand', 'category', 'region'),)

    @property
    def min_online_price(self):
        request_url = "{0}/{1}".format(
            CRAWLED_HOST, CRAWLED_URN.format(product_id=self.product_id)
        )
        resp = requests.get(request_url)
        resp_json = resp.json()
        return resp_json['min_price'] or 0

    @property
    def max_online_price(self):
        request_url = "{0}/{1}".format(
            CRAWLED_HOST, CRAWLED_URN.format(product_id=self.product_id)
        )
        resp = requests.get(request_url)
        resp_json = resp.json()
        return resp_json['max_price'] or 0

    @property
    def seller_prices(self):
        urn = "product/{product_id}/".format(product_id=self.product_id)
        headers = {
            "Access-Token": 'pxfe15uguhtd54c82u9gdkd27mlbhwoi',
            "Client-Key": 'cb5a4b9e5de0ee57647aed56f9295546',
            "Region-Id": self.region_id,
            "Latitude": 0,
            "Longitude": 0,
            "x-api-version": "1.3"
        }
        response = requests.get("{0}/{1}".format(PRICES_HOST, urn), headers=headers)
        resp_json = response.json()
        store_prices = []
        try:
            for store in resp_json.get('stores'):
                store_prices.append({
                    'store_id': store['id'],
                    'price':  store['price'],
                    'is_lfr': True if store['chain_id'] else False
                })
        except TypeError as exc:
            pass
        return store_prices or []


class Store(models.Model):
    store_id = models.IntegerField()
    region = models.ForeignKey(Region)

    def __unicode__(self):
        return u'{0}'.format(self.store_id)


class SuggestedPrices(models.Model):
    product = models.ForeignKey(Product)
    store = models.ForeignKey(Store)
    responsible_factor = models.ForeignKey(VariationFactor)
    suggested_price = models.FloatField()
