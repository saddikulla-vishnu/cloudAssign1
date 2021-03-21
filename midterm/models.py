from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Household(models.Model):
    hshd_num = models.PositiveIntegerField(unique=True, primary_key=True)
    loyalty_flag = models.CharField(max_length=4, null=True, blank=True)
    age_range = models.CharField(max_length=16, null=True, blank=True)
    marital_status = models.CharField(max_length=16, null=True, blank=True)
    income_range = models.CharField(max_length=32, null=True, blank=True)
    homeowner_desc = models.CharField(max_length=32, null=True, blank=True)
    hshd_composition = models.CharField(max_length=32, null=True, blank=True)
    hshd_size = models.CharField(max_length=32, null=True, blank=True)
    children = models.CharField(max_length=32, null=True, blank=True)
    #  uid = models.ForeignKey(User, db_column='uid', db_constraint=False, on_delete=models.DO_NOTHING, null=True, blank=True)
    #  upload_date_time = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'households'

    def __str__(self):
        return str(self.hshd_num)


class Transaction(models.Model):
    hshd_num = models.ForeignKey('Household', db_column='hshd_num', db_constraint=False, on_delete=models.DO_NOTHING)
    basket_num = models.PositiveIntegerField(null=True, blank=True)
    date = models.CharField(max_length=32, null=True, blank=True)
    product_num = models.ForeignKey('Product', db_column='product_num', db_constraint=False, on_delete=models.DO_NOTHING)
    spend = models.FloatField(null=True, blank=True)
    units = models.IntegerField(null=True, blank=True)
    store_region = models.CharField(max_length=32, null=True, blank=True)
    week_num = models.PositiveIntegerField(null=True, blank=True)
    year = models.PositiveIntegerField(null=True, blank=True)
    #  uid = models.ForeignKey(User, db_column='uid', db_constraint=False, on_delete=models.DO_NOTHING)
    #  upload_date_time = models.DateTimeField(null=True, blank=True)


    class Meta:
        db_table = 'transactions'


class Product(models.Model):
    PRIVATE_TYPE, NATURAL_TYPE = range(2)
    NATURAL_FOOD, ORGANIC_FOOD = range(2)
    BRAND_TYPE_CHOICES = (
        (PRIVATE_TYPE, 'Private'),
        (NATURAL_TYPE, 'National')
    )
    NATURAL_ORGANIC_FLAG_CHOICES = (
        (NATURAL_FOOD, 'Natural'),
        (ORGANIC_FOOD, 'Organic')
    )

    product_num = models.PositiveIntegerField(unique=True, primary_key=True)
    department = models.CharField(max_length=32, null=True, blank=True)
    commodity = models.CharField(max_length=32, null=True, blank=True)
    brand_type = models.CharField(max_length=32, null=True, blank=True)
    natural_organic_flag = models.CharField(max_length=32, null=True, blank=True)
    #  uid = models.ForeignKey(User, db_column='uid', db_constraint=False, on_delete=models.DO_NOTHING)
    #  upload_date_time = models.DateTimeField(null=True, blank=True)


    class Meta:
        db_table = 'products'

    def __str__(self):
        return str(self.product_num)
