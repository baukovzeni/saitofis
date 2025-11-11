from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import SaleItem
from decimal import Decimal
@receiver(post_save, sender=SaleItem)
def recalc_total_on_save(sender, instance, created, **kwargs):
    sale=instance.sale
    total=sum(i.subtotal for i in sale.items.all())
    sale.total=total; sale.save(update_fields=['total'])
    if created:
        p=instance.product; p.stock=max(0, p.stock-instance.qty); p.save(update_fields=['stock'])
@receiver(post_delete, sender=SaleItem)
def recalc_total_on_delete(sender, instance, **kwargs):
    sale=instance.sale
    total=sum(i.subtotal for i in sale.items.all())
    sale.total=total; sale.save(update_fields=['total'])
    p=instance.product; p.stock=p.stock+instance.qty; p.save(update_fields=['stock'])
