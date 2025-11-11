from django import forms
from .models import Product

class ProductSearchForm(forms.Form):
    q = forms.CharField(label='Поиск', required=False)

class ProductForm(forms.ModelForm):  # ← NEW
    class Meta:
        model = Product
        fields = ('name', 'category', 'price', 'stock', 'is_active', 'image')