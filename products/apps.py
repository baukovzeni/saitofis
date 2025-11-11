from django.apps import AppConfig

class ProductsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'products'
    # ready() можно не трогать, если signals не используешь
    # def ready(self):
    #     from . import signals  # noqa