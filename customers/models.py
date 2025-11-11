from django.db import models
class Customer(models.Model):
    name=models.CharField('Имя', max_length=120)
    phone=models.CharField('Телефон', max_length=32, blank=True)
    email=models.EmailField('Email', blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    class Meta: ordering=['name']; verbose_name='Клиент'; verbose_name_plural='Клиенты'
    def __str__(self): return self.name
