from rest_framework.test import APIRequestFactory, APITestCase
from rest_framework import status
import json
from django.test.testcases import TestCase
from django.db import models
from src.smart_price.models import VariationRule, DiscountRule, VariationFactor

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

    def setup(self):
        """
        Test Case that checks the validity of our tasks module
        :return:
        """
        Variationruleobj=VariationRule.objects.create(rule_name='test_rule', rule_operator='%')
        DiscountRule.objects.create(name='testing', value=2, discount_op='Flat')
        brandobj=Brand.objects.create(name='LG')
        VariationFactor.objects.create(name='variation_factor', factor_value='2', factor_types=Variationruleobj, factor_target=brandobj)

