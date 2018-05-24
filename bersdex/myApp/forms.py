from django import forms
from django.forms import CheckboxInput
from .models import Products,Category


class ProductForm(forms.ModelForm):
    

    class Meta:
        model = Products
        fields = [
            'title',
            'body',
            'image',
            'is_original',
            'prod_date',
            'features',
            'sizes',
            'category'
        ]
        labels = {
            'title': ('Title'),
            'body': ('Body'),
            'image': ('Image'),
            'is_original': ('Original/Replica'),
            'prod_date': ('Product Date'),
            'features': ('Features'),
            'sizes': ('Sizes(width*height)'),
            'category': ('Category')
        }

