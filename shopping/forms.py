from django import forms

from django.forms.widgets import HiddenInput

from .models import Customer, Order, Product, Product_unit, Category

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'title',
            'image',
            'description',
            'category',
            'price',
            'stock',
            'show',
            'weight_measurement',
            'weight',
            'number_sales',
        ]
        widgets = {'number_sales' : forms.HiddenInput(),
                   'category': forms.HiddenInput(),}



class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = [
            'title',
            'image',
            'description',
        ]


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = [
            'company_name',
            'rfc',
            'country',
            'state',
            'city',
            'colony',
            'postal_code',
            'street',
            'number',
            'phone_number',
            'email',
        ]

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        exclude = ['products']
        fields = [
            'customer',
            'status',
            'subtotal_cost',
            'total_cost',
            'details',
        ]
        widgets = {'subtotal_cost' : forms.HiddenInput(),
                   'total_cost'    : forms.HiddenInput(),
        }

class Product_unitForm(forms.ModelForm):
    class Meta:
        model = Product_unit
        fields = [
            'product',
            'quantity',
        ]

        widgets = {'product': forms.HiddenInput()}
