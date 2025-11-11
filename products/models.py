# products/models.py
from django.db import models
from django.core.validators import FileExtensionValidator   # <-- ДОБАВИЛИ

class Category(models.Model):
    name = models.CharField(max_length=120, unique=True)
    def __str__(self): return self.name

class Product(models.Model):
    sku       = models.CharField("Артикул", max_length=50, unique=True)
    name      = models.CharField("Название", max_length=200)
    category  = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    price     = models.DecimalField("Цена", max_digits=10, decimal_places=2, default=0)
    stock     = models.IntegerField("Остаток", default=0)
    is_active = models.BooleanField("Активен", default=True)

    # ВМЕСТО ImageField — FileField, Pillow не требуется
    image = models.FileField(
        "Фото",
        upload_to="product_photos/",
        blank=True, null=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif', 'webp'])]
    )

    def __str__(self):
        return f"{self.name} ({self.sku})"