from django.db import models
from django.contrib.auth.models import User

# Create your models here.

STATUS = (
    ('available', 'available'),
    ('expired', 'expired'),
)


class Category(models.Model):
    # field name
    category_name = models.CharField(max_length=120, unique=True)
    # create_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.category_name


class Product(models.Model):
    # field name
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=120, verbose_name="Product Name", unique=True)
    product_code = models.CharField(max_length=10, verbose_name="Product Code")
    price = models.PositiveIntegerField(verbose_name="Price")
    price_updated = models.DateTimeField(blank=True, null=True)
    category_id = models.ForeignKey(Category, verbose_name="Category Name", on_delete=models.CASCADE, null=True)
    manufacturing_date = models.DateField(verbose_name="Manufacturing Date")
    expiry_date = models.DateField(verbose_name="Expiry Date")
    status = models.CharField(choices=STATUS, max_length=50)

    # create_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
