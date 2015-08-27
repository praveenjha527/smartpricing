import operator
from django.contrib import contenttypes
from .models import *

import mimetypes
# import django_rq
# from django_rq import job
from datetime import timedelta
from django.conf import settings
from django.core.mail import send_mail
from .models import Product
from schedule import schedule_once

# def dynamic_price_calculation():
#     """
#     This will dynamically calculate the prices of products on the various parameters and offsets
#     :return:
#     """
#     resultant_prices={}
#     all_products=Product.objects.all()
#     for product in all_products:
#         product_id=product.product_id
#         brand_id=product.brand_id
#         category_id=product.category_id
#         region_id=product.region_id
#         seller_prices=product.seller_prices
#         if seller_prices:
#             lsp=min([x['price'] for x in seller_prices if not x['is_lfr']])
#             lsp_stores = filter(lambda x : x==lsp and not x['is_lfr'], seller_prices)
#             #todo get from dashboard or auto generated V
#             lsp_store_factor=10
#             V=lsp_store_factor
#             V_amount=(V*lsp)/100
#             lsp_near_stores=filter(lambda x : x['price'] <=lsp+V_amount, seller_prices)
#
#             min_online_price=product.min_online_price
#
#             zopper_selling_prices=lsp
#
#             if min_online_price !=0:
#                 # this will be dependent  on other factors like trasfer price,etc
#                 zopper_selling_prices=min_online_price-1
#
#             if zopper_selling_prices > lsp:
#                 zopper_selling_prices = lsp
#
#
#             # lfr stores
#             lfr_stores=filter(lambda x: x['is_lfr'],seller_prices)
#             if lfr_stores:
#                 lfr_lsp=min([x['price'] for x in seller_prices if x['is_lfr']])
#                 lfr_lsp_stores= filter(lambda x : x['price']==lfr_lsp,lfr_stores)
#                 lfr_lsp_near_stores=filter(lambda x : x['price'] < lfr_lsp,lfr_stores)
#
#             for item in seller_prices:
#                 if item['is_lfr']:
#                     if item in lfr_lsp_stores:
#                         resultant_prices[item['store_id']]=zopper_selling_prices
#
#                     elif item in lfr_lsp_near_stores:
#                         resultant_prices[item['store_id']]=item['price']-abs(zopper_selling_prices-lsp)
#                     else:
#                         resultant_prices[item['store_id']]=item['price']
#                 else:
#                     if item in lsp_near_stores:
#                         resultant_prices[item['store_id']]=item['price']-abs(zopper_selling_prices-lfr_lsp)
#                     else:
#                         resultant_prices[item['store_id']]=item['price']
#
#
#
#
#
#
#
#
#
#
#
#
# schedule_once(dynamic_price_calculation,interval=60*30)
#


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