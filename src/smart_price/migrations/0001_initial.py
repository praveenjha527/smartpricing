# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('category_id', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='DiscountRule',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('value', models.IntegerField()),
                ('discount_op', models.CharField(max_length=1, choices=[(b'-', b'Flat'), (b'%', b'Percentage')])),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('product_id', models.IntegerField()),
                ('brand', models.ForeignKey(related_name='products', to='smart_price.Brand')),
                ('category', models.ForeignKey(related_name='products', to='smart_price.Category')),
            ],
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('region_id', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Store',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('store_id', models.IntegerField()),
                ('region', models.ForeignKey(to='smart_price.Region')),
            ],
        ),
        migrations.CreateModel(
            name='SuggestedPrices',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('suggested_price', models.FloatField()),
                ('product', models.ForeignKey(to='smart_price.Product')),
            ],
        ),
        migrations.CreateModel(
            name='VariationFactor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('factor_value', models.FloatField()),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
        ),
        migrations.CreateModel(
            name='VariationRule',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('rule_name', models.CharField(max_length=255)),
                ('rule_operator', models.CharField(max_length=1)),
            ],
        ),
        migrations.AddField(
            model_name='variationfactor',
            name='factor_types',
            field=models.ForeignKey(related_name='factors', to='smart_price.VariationRule'),
        ),
        migrations.AddField(
            model_name='variationfactor',
            name='variation_discount',
            field=models.ForeignKey(to='smart_price.DiscountRule'),
        ),
        migrations.AddField(
            model_name='suggestedprices',
            name='responsible_factor',
            field=models.ForeignKey(to='smart_price.VariationFactor'),
        ),
        migrations.AddField(
            model_name='suggestedprices',
            name='store',
            field=models.ForeignKey(to='smart_price.Store'),
        ),
        migrations.AddField(
            model_name='product',
            name='region',
            field=models.ForeignKey(related_name='products', to='smart_price.Region'),
        ),
        migrations.AlterUniqueTogether(
            name='product',
            unique_together=set([('product_id', 'brand', 'category', 'region')]),
        ),
    ]
