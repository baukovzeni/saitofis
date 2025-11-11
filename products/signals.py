# products/signals.py
import os
from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver
from django.core.files.storage import default_storage
from .models import Product

def _safe_delete(path: str):
    """Удаляет файл из стораджа, если он существует."""
    if not path:
        return
    try:
        if default_storage.exists(path):
            default_storage.delete(path)
    except Exception:
        # тихо игнорируем, чтобы не ронять запрос
        pass

@receiver(pre_save, sender=Product)
def delete_old_image_on_change(sender, instance: Product, **kwargs):
    """
    Если у продукта меняется image (новый файл либо очистка поля),
    удаляем старый файл из MEDIA.
    """
    if not instance.pk:
        return  # новый объект — нечего удалять

    try:
        old = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        return

    old_file = getattr(old.image, "name", "")
    new_file = getattr(instance.image, "name", "")

    # изменили файл или очистили поле -> удаляем старый
    if old_file and old_file != new_file:
        _safe_delete(old_file)

@receiver(post_delete, sender=Product)
def delete_image_on_product_delete(sender, instance: Product, **kwargs):
    """
    При удалении продукта удаляем файл изображения.
    """
    file_name = getattr(instance.image, "name", "")
    if file_name:
        _safe_delete(file_name)
