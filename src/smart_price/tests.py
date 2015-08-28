from rest_framework.test import APIRequestFactory, APITestCase
from rest_framework import status
import json
from django.test import TestCase
from models import *
from tasks import *

factory = APIRequestFactory()
class Apitest(APITestCase):
     def test_get_data(self):
        """
        Ensure we can get the right format.
        """
        response = self.client.get('/suggested_prices/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content), [{"product":{"product_id":39,"seller_prices":[],"min_online_price":7999.0,"max_online_price":18586.0,"brand":"Blackberry","category":637},"store":{"store_id":73},"region_id":1,"suggested_price":899.0},{"product":{"product_id":50,"seller_prices":[],"min_online_price":8400.0,"max_online_price":34990.0,"brand":"Blackberry","category":637},"store":{"store_id":73},"region_id":1,"suggested_price":1299.0}])

class TasksTest(TestCase):

    def setUp(self):
        """
        Test Case that checks the validity of our tasks module
        :return:
        """
        Variationruleobj=VariationRule.objects.create(rule_name='test_rule', rule_operator='%')
        discountObj=DiscountRule.objects.create(name='testing', value=2, discount_op='Flat')
        brandobj=Brand.objects.create(name='Sony')
        VariationFactor.objects.create(name='variation_factor', factor_value='2', factor_types=Variationruleobj, factor_target=brandobj, variation_discount=discountObj)
        catobj=Category.objects.create(category_id=208)
        regionobj=Region.objects.create(region_id=1)
        product=Product.objects.create(product_id=9297316,category=catobj,region=regionobj,brand=brandobj)
        store=Store.objects.create(store_id=93256, region=regionobj)

    def test_process_all(self):
        RuleProcessor().process_all()
        prod_obj=Product.objects.get(product_id=9297316)
        brandobj=Brand.objects.get(name='Sony')
        Variationruleobj=VariationRule.objects.get(rule_name='test_rule', rule_operator='%')
        store_obj=Store.objects.get(store_id=93256)
        responsible_factor=VariationFactor.objects.get(name='variation_factor', factor_value='2',\
                           factor_types=Variationruleobj)
        suggested_price_obj=SuggestedPrices(product=prod_obj,store=store_obj,responsible_factor=responsible_factor)
        suggested_price=suggested_price_obj.suggested_price
        self.assertEqual(suggested_price,60180)
        