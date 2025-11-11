from django import forms
from django.forms import inlineformset_factory
from .models import Sale, SaleItem
from products.models import Product
class SaleForm(forms.ModelForm):
    class Meta: model=Sale; fields=('customer','payment_method')
class SaleItemForm(forms.ModelForm):
    product=forms.ModelChoiceField(queryset=Product.objects.filter(is_active=True).order_by('name'))
    class Meta: model=SaleItem; fields=('product','qty','price','subtotal')
    def clean(self):
        data=super().clean(); qty=data.get('qty') or 0; price=data.get('price') or 0; data['subtotal']=qty*price; return data
SaleItemFormSet=inlineformset_factory(Sale, SaleItem, form=SaleItemForm, extra=1, can_delete=True, min_num=1, validate_min=True)
