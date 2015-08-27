from .models import *

import mimetypes
# import django_rq
# from django_rq import job
from datetime import timedelta
from django.conf import settings
from django.core.mail import send_mail
import mandrill
from .models import Product
from schedule import schedule_once


##This will dynamically calculate the prices of products on the various parameters and offsets



def dynamic_price_calculation:
    resultant_prices={}
    all_products=Product.objects.all()
    for product in all_products:
        product_id=product.product_id
        brand_id=product.brand_id
        category_id=product.category_id
        region_id=product.region_id
        seller_prices=product.seller_prices
        if seller_prices:
            lsp=min([x['price'] for x in seller_prices if not x['is_lfr']])
            lsp_stores=filter(lambda x : x==lsp and not x['is_lfr'],seller_prices)
            #todo get from dashboard or auto generated V
            lsp_store_factor=10
            V=lsp_store_factor
            V_amount=(V*lsp)/100
            lsp_near_stores=filter(lambda x : x['price'] <=lsp,seller_prices)

            min_online_price=product.min_online_price

            zopper_selling_prices=lsp

            if min_online_price !=0:
                # this will be dependent  on other factors like trasfer price,etc
                zopper_selling_prices=min_online_price-1

            if zopper_selling_prices > lsp:
                zopper_selling_prices= lsp


            # lfr stores
            lfr_stores=filter(lambda x: x['is_lfr'],seller_prices)
            if lfr_stores:
                lfr_lsp=min([x['price'] for x in seller_prices if x['is_lfr']])
                lfr_lsp_stores= filter(lambda x : x['price']==lfr_lsp,lfr_stores)
                lfr_lsp_near_stores=filter(lambda x : x['price'] < lfr_lsp,lfr_stores)

            for item in seller_prices:
                if item['is_lfr']:
                    if item in lfr_lsp_stores:
                        resultant_prices[item['store_id']]=zopper_selling_prices

                    elif item in lfr_lsp_near_stores:
                        resultant_prices[item['store_id']]=item['price']-abs(zopper_selling_prices-lsp)
                    else:
                        resultant_prices[item['store_id']]=item['price']
                else:
                    if item in lsp_near_stores:
                        resultant_prices[item['store_id']]=item['price']-abs(zopper_selling_prices-lfr_lsp)
                    else:
                        resultant_prices[item['store_id']]=item['price']












schedule_once(dynamic_price_calculation,interval=60*30)

