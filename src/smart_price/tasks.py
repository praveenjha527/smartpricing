import operator
from django.contrib import contenttypes
from .models import *

import mimetypes
import django_rq
from django_rq import job
from datetime import timedelta
from django.conf import settings
from django.core.mail import send_mail
from .models import Product
from schedule import schedule_once

def dynamic_price_calculation():
    RuleProcessor().process_all()


class RuleProcessor(object):
    queryset = VariationFactor.objects.all()

    # def prepare_prices(self, seller_prices):
    #     categorized_price = {
    #     }
    #     for price_dict in seller_prices:
    #         store_list = categorized_price.get(price_dict['price'], [])
    #         store_list.append(price_dict['store_id'])
    #         categorized_price[price_dict['price']] = store_list
    #     return categorized_price

    def get_factor_target_query_set(self, factor_target):
        product_content_type = contenttypes.models.ContentType.objects.get_for_model(Product)

        if product_content_type == contenttypes.models.ContentType.objects.get_for_model(factor_target):
                return_query_set = factor_target.all()
        else:
                return_query_set = factor_target.products.all()
        return return_query_set

    def process_all(self):
        reduction_factor = 1
        # product_prices = {}
        for record in self.queryset:

            factor_target = record.factor_target
            loop_query_set = self.get_factor_target_query_set(factor_target)

            for product in loop_query_set:
                seller_prices = product.seller_prices
                # product_prices = self.prepare_prices(seller_prices)
                min_price = min([price_dict['price'] for price_dict in seller_prices])
                processed_variation = self.process_variation(record, min_price)
                for price_dict in seller_prices:
                    if (price_dict['price'] - min_price) <= processed_variation:
                        SuggestedPrices.objects.create(
                            product=product, responsible_factor=record,
                            suggested_price=product.min_online_price - reduction_factor,
                            store=Store.objects.get_or_create(
                                store_id=price_dict['store_id'], region=product.region)
                        )

    def process_variation(self, variation_factor, price):
        value = variation_factor.factor_value
        op = variation_factor.factor_types.rule_operator
        processed_variation = 0
        if op in ['-', '/']:
            processed_variation = self.get_operator(op)(price, value)
        else:
            processed_variation = self.get_operator(op)(value, price)
        return processed_variation

    def get_operator(self, op):
        return {
            '+': operator.add,
            '-': operator.sub,
            '*': operator.mul,
            '/': operator.div,
            '%': self.__calculate_percentage__,
        }[op]

    def __calculate_percentage__(self, val1, val2):
        return (val1/100) * val2

########################ADD TASK TO SCHEDULER ##############################
from schedule import schedule_once
schedule_once(dynamic_price_calculation,interval=60*30)