from django.db import models
from django.contrib.auth import get_user_model
from products.models import Product
from customers.models import Customer
User = get_user_model()
class Sale(models.Model):
    PAYMENT_CHOICES=(('cash','Наличные'),('card','Карта'),('transfer','Перевод'))
    cashier = models.ForeignKey(User, on_delete=models.PROTECT, related_name='sales')
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=16, choices=PAYMENT_CHOICES, default='cash')
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    class Meta: ordering=['-id']; verbose_name='Продажа'; verbose_name_plural='Продажи'
    def __str__(self): return f"Sale #{self.id}"
class SaleItem(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    qty = models.PositiveIntegerField('Кол-во', default=1)
    price = models.DecimalField('Цена', max_digits=10, decimal_places=2)
    subtotal = models.DecimalField('Сумма', max_digits=12, decimal_places=2)
    def __str__(self): return f"{self.product} x{self.qty}"
