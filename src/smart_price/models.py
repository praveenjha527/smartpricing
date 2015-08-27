from django.db import models

class Price(models.Model):
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
        pass