import requests
from django.db import models

PRICES_HOST = "http://45.56.112.85"

CRAWLED_HOST = "http://128.199.238.212/"
CRAWLED_URN = "product/minprice/{product_id}/"

class Product(models.Model):
    product_id = models.IntegerField()
    brand = models.CharField(max_length=255)
    category_id = models.IntegerField()
    region_id = models.IntegerField()


    @property
    def minprice(self):
        request_url = "{0}/{1}".format(
            CRAWLED_HOST, CRAWLED_URN.format(product_id=self.product_id)
        )
        resp = requests.get(request_url)
        resp_json = resp.json()
        return resp_json['min_price']

    @property
    def maxprice(self):
        request_url = "{0}/{1}".format(
            CRAWLED_HOST, CRAWLED_URN.format(product_id=self.product_id)
        )
        resp = requests.get(request_url)
        resp_json = resp.json()
        return resp_json['max_price']

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
        return store_prices


