
from django.contrib import admin

from product.models import Category, Product


class CategoryAdmin(admin.ModelAdmin):

    list_display = [
        'category_name',
    ]


class ProductAdmin(admin.ModelAdmin):

    list_display = [
        'user_id',
        'name',
        'product_code',
        'price',
        'category_id',
        'manufacturing_date',
        'expiry_date',
        'status',
    ]


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
