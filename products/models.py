from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=120, unique=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='children')
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
    def __str__(self): return self.name

class Product(models.Model):
    sku = models.CharField('Артикул', max_length=64, unique=True)
    name = models.CharField('Наименование', max_length=200)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='products')
    price = models.DecimalField('Цена', max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField('Остаток', default=0)
    is_active = models.BooleanField('Активен', default=True)
    image = models.ImageField('Фото', upload_to='product_photos/', blank=True, null=True)  # ← NEW
    image = models.ImageField(upload_to='product_photos/', null=True, blank=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
    def __str__(self): return f"{self.name} ({self.sku})"