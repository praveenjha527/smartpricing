import requests
from django.db import models

STORES_HOST = "http://45.56.118.218"


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
    def sellerprices(self):
        urn="api/v1/getproductpricestore/{product_id}/".format(product_id=self.product_id)
        params = {
            "latitude":0,
            "longitude":0,
            "region_id":self.region_id
        }
        response = requests.get("{0}/{1}".format(STORES_HOST, urn), params=params)