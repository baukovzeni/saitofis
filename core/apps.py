from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.db import connection

class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        from .initial_setup import run_initial_setup
        def handler(**kwargs):
            # ждём пока создадутся таблицы бизнес-приложений
            required = {'products_category','products_product','customers_customer','sales_sale','sales_saleitem'}
            existing = set(connection.introspection.table_names())
            if not required.issubset(existing):
                return  # ещё рано — дождёмся следующего post_migrate
            run_initial_setup()
        post_migrate.connect(handler, dispatch_uid='core_post_migrate_autosetup')
