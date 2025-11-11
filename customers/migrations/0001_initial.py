from django.db import migrations, models

class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                    ('name', models.CharField(max_length=120, verbose_name='Имя')),
                    ('phone', models.CharField(blank=True, max_length=32, verbose_name='Телефон')),
                    ('email', models.EmailField(blank=True, max_length=254, verbose_name='Email')),
                    ('created_at', models.DateTimeField(auto_now_add=True))],
            options={'ordering':['name'],'verbose_name':'Клиент','verbose_name_plural':'Клиенты'}
        )
    ]
