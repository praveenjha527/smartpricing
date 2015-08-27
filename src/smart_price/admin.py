__author__ = 'praveen'
from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from models import Product, Category, VariationFactor, VariationRule, Region, Brand


class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_id', 'brand', 'category', 'region', 'variation_factors',)
    list_filter = ('product_id', 'brand', 'category', 'region',)
    search_fields = ('product_id',)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_id',)
    list_filter = ('category_id',)
    search_fields = ('categry_id',)


class FactorInline(GenericTabularInline):
    model = VariationFactor


class VariationFactorAdmin(admin.ModelAdmin):
    inlines = [
        FactorInline,
    ]
    list_display = ('factor_value', 'factor_types', 'rule_weight', 'factor_target',)
    list_filter = ('factor_value', 'factor_types', 'rule_weight')
    search_fields = ('factor_value',)


class VariationRuleAdmin(admin.ModelAdmin):
    list_display = ('rule_name', 'rule_operator', )
    list_filter = ('rule_name',)


class BrandAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


class RegionAdmin(admin.ModelAdmin):
    list_display = ('region_id',)
    search_fields = ('region_id',)


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(VariationFactor, VariationFactorAdmin)
admin.site.register(Region, RegionAdmin)
admin.site.register(Brand, BrandAdmin)
admin.site.register(VariationRule, VariationRuleAdmin)
