import requests
from django.db import models

PRICES_HOST = "http://45.56.112.85"


class Product(models.Model):
    product_id = models.IntegerField()
    brand_id = models.IntegerField()
    category_id = models.IntegerField()
    region_id = models.IntegerField()


    @property
    def minprice(self):
        pass

    @property
    def maxprice(self):
        pass

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
        store_prices =[]
        for store in resp_json.get('stores'):
            store_prices.append({
                'store_id': store['id'],
                'price':  store['price']
            })

        return store_prices
