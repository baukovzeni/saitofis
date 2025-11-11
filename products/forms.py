from django import forms
from .models import Product


class ProductSearchForm(forms.Form):
    q = forms.CharField(label='Поиск', required=False)


class ProductForm(forms.ModelForm):
    # FileField вместо ImageField, чтобы не требовался Pillow
    image = forms.FileField(
        required=False,
        widget=forms.ClearableFileInput(attrs={'accept': 'image/*'})
    )

    class Meta:
        model = Product
        # добавь/убери поля под свою модель, но image обязательно оставить
        fields = ['sku', 'name', 'category', 'price', 'stock', 'is_active', 'image']