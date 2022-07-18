from django.forms.widgets import DateInput
from django import forms
from .models import Category, Product
from datetime import datetime


class CategoryForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')

        super(CategoryForm, self).__init__(*args, **kwargs)

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    def clean(self):
        cleaned_data = super(CategoryForm, self).clean()
        return cleaned_data

    class Meta:
        model = Category
        fields = ('category_name',)


class ProductForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')

        super(ProductForm, self).__init__(*args, **kwargs)
        # add class
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        datetime.today().strftime('%Y-%m-%d')

    def clean(self):
        cleaned_data = super(ProductForm, self).clean()
        if cleaned_data.get("manufacturing_date") > cleaned_data.get('expiry_date'):
            raise forms.ValidationError({"expiry_date": "Please select valid expiry date"})
        return cleaned_data

    class Meta:
        model = Product
        fields = ('name', 'product_code', 'price', 'category_id', 'manufacturing_date', 'expiry_date', 'status')
        widgets = {
            'manufacturing_date': DateInput(attrs={'type': 'date', "max": datetime.today().strftime('%Y-%m-%d')}),
            'expiry_date': DateInput(attrs={'type': 'date'}),
        }
