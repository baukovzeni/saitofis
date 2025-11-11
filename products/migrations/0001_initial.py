from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                    ('name', models.CharField(max_length=120, unique=True)),
                    ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='children', to='products.category'))],
            options={'verbose_name':'Категория','verbose_name_plural':'Категории'}
        ),
        migrations.CreateModel(
            name='Product',
            fields=[('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                    ('sku', models.CharField(max_length=64, unique=True, verbose_name='Артикул')),
                    ('name', models.CharField(max_length=200, verbose_name='Наименование')),
                    ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Цена')),
                    ('stock', models.PositiveIntegerField(default=0, verbose_name='Остаток')),
                    ('is_active', models.BooleanField(default=True, verbose_name='Активен')),
                    ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='products', to='products.category'))],
            options={'ordering':['name'],'verbose_name':'Товар','verbose_name_plural':'Товары'}
        ),
    ]
