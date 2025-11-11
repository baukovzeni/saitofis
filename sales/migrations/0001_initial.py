from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings

class Migration(migrations.Migration):
    initial = True
    dependencies = [
        ('customers','0001_initial'),
        ('products','0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]
    operations = [
        migrations.CreateModel(
            name='Sale',
            fields=[('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                    ('created_at', models.DateTimeField(auto_now_add=True)),
                    ('payment_method', models.CharField(choices=[('cash','Наличные'),('card','Карта'),('transfer','Перевод')], default='cash', max_length=16)),
                    ('total', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                    ('cashier', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='sales', to=settings.AUTH_USER_MODEL)),
                    ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='customers.customer'))],
            options={'ordering':['-id'],'verbose_name':'Продажа','verbose_name_plural':'Продажи'}
        ),
        migrations.CreateModel(
            name='SaleItem',
            fields=[('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                    ('qty', models.PositiveIntegerField(default=1, verbose_name='Кол-во')),
                    ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Цена')),
                    ('subtotal', models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Сумма')),
                    ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='products.product')),
                    ('sale', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='sales.sale'))],
        ),
    ]
