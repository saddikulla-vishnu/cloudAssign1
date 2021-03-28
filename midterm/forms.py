import csv
from itertools import islice

from django import forms

from .models import Household, Transaction, Product

class SearchForm(forms.Form):
    ORDER_BY_CHOICES = (
        (None, '-------------'),
        ('1', 'Household Number'),
        ('2', 'Basket Number'),
        ('3', 'Date'),
        ('4', 'Product Number'),
        ('5', 'Department'),
        ('6', 'Commodity')
    )
    hshd_num = forms.CharField(
        label="Household Number",
        widget=forms.TextInput(attrs={"class": "form-control"}),
        required=False
    )
    order_by = forms.CharField(
        label="Sort By",
        widget=forms.Select(choices=ORDER_BY_CHOICES, attrs={"class": "form-control"}),
        required=False
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label

class UploadForm(forms.Form):
    hshds_file = forms.FileField(label='Upload Household Data', required=False)
    transactions_file = forms.FileField(label='Upload Transaction Data', required=False)
    products_file = forms.FileField(label='Upload Product Data', required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['hshds_file'].widget.attrs = {"class": "form-control col-6"}
        self.fields['transactions_file'].widget.attrs = {"class": "form-control col-6"}
        self.fields['products_file'].widget.attrs = {"class": "form-control col-6"}

    def save(self, *args, **kwargs):
        HSHD_COLUMN_MAPPING = {
            'HSHD_NUM': 'hshd_num',
            'L': 'loyalty_flag',
            'AGE_RANGE': 'age_range',
            'MARITAL': 'marital_status',
            'INCOME_RANGE': 'income_range',
            'HOMEOWNER': 'homeowner_desc',
            'HSHD_COMPOSITION': 'hshd_composition',
            'HH_SIZE': 'hshd_size',
            'CHILDREN': 'children',
        }
        TRANSACTION_COLUMN_MAPPING = {
            'BASKET_NUM': 'basket_num',
            'HSHD_NUM': 'hshd_num_id',
            'PURCHASE_': 'date',
            'PRODUCT_NUM': 'product_num_id',
            'SPEND': 'spend',
            'UNITS': 'units',
            'STORE_R': 'store_region',
            'WEEK_NUM': 'week_num',
            'YEAR': 'year',
        }
        PRODUCT_COLUMN_MAPPING = {
            'PRODUCT_NUM': 'product_num',
            'DEPARTMENT': 'department',
            'COMMODITY': 'commodity',
            'BRAND_TY': 'brand_type',
            'NATURAL_ORGANIC_FLAG': 'natural_organic_flag',
        }

        transactions_file = self.cleaned_data.get('transactions_file')
        if transactions_file:
            transactions_file = transactions_file.read().decode('utf-8').splitlines()
            transaction_data = [{TRANSACTION_COLUMN_MAPPING.get(k.strip()): v.strip() for k, v in row.items()} for row in csv.DictReader(transactions_file, skipinitialspace=True)]
            batch_size = 100000
            objs = (Transaction(**_trnsctn) for _trnsctn in transaction_data)
            while True:
                batch = list(islice(objs, batch_size))
                if not batch:
                    break
                Transaction.objects.bulk_create(batch, batch_size)

        hshds_file = self.cleaned_data.get('hshds_file')
        if hshds_file:
            hshds_file = hshds_file.read().decode('utf-8').splitlines()
            hshd_data = [{HSHD_COLUMN_MAPPING.get(k.strip()): v.strip() for k, v in row.items()} for row in csv.DictReader(hshds_file, skipinitialspace=True)]
            batch_size = 100000

            # Start: Filter out already existing housholds
            existing_hshd_nums = set(Household.objects.values_list('hshd_num', flat=True))
            hshd_data = [_hshd for _hshd in hshd_data if int(_hshd['hshd_num']) not in existing_hshd_nums]
            # End: Filter out already existing housholds

            objs = (Household(**_hshd) for _hshd in hshd_data)
            while True:
                batch = list(islice(objs, batch_size))
                if not batch:
                    break
                Household.objects.bulk_create(batch, batch_size)

        products_file = self.cleaned_data.get('products_file')
        if products_file:
            products_file = products_file.read().decode('utf-8').splitlines()
            product_data = [{PRODUCT_COLUMN_MAPPING.get(k.strip()): v.strip() for k, v in row.items()} for row in csv.DictReader(products_file, skipinitialspace=True)]
            batch_size = 100000

            # Start: Filter out already existing products
            existing_product_nums = set(Product.objects.values_list('product_num', flat=True))
            product_data = [_prdct for _prdct in product_data if int(_prdct['product_num']) not in existing_product_nums]
            # End: Filter out already existing products

            objs = (Product(**_product) for _product in product_data)
            while True:
                batch = list(islice(objs, batch_size))
                if not batch:
                    break
                Product.objects.bulk_create(batch, batch_size)
