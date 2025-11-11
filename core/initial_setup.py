# core/initial_setup.py
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.db import transaction
from products.models import Category, Product
from sales.models import Sale, SaleItem
import os

def run_initial_setup():
    """
    Вызывается из post_migrate. Должен быть идемпотентным, ничего не падать,
    когда данные уже есть.
    """
    if os.getenv("SKIP_INITIAL_SETUP") == "1":
        return

    with transaction.atomic():
        ensure_groups_and_permissions()
        ensure_users()
        ensure_demo_data()  # <-- теперь эта функция существует и делает сиды

def ensure_groups_and_permissions():
    # Группа кассиров (продавцов)
    seller_group, _ = Group.objects.get_or_create(name="seller")
    # Группа админов магазина
    admin_group, _ = Group.objects.get_or_create(name="store_admin")

    # Разрешения на модели
    # Пример: продавцу — чтение/добавление продаж и просмотр товаров, администратору — всё.
    sale_ct = ContentType.objects.get_for_model(Sale)
    product_ct = ContentType.objects.get_for_model(Product)
    category_ct = ContentType.objects.get_for_model(Category)

    perms_codes = {
        "sale": ["add_sale", "change_sale", "delete_sale", "view_sale"],
        "product": ["add_product", "change_product", "delete_product", "view_product"],
        "category": ["add_category", "change_category", "delete_category", "view_category"],
    }
    perms = {}
    for model, codes in perms_codes.items():
        for code in codes:
            try:
                perms[code] = Permission.objects.get(codename=code)
            except Permission.DoesNotExist:
                # Если прав нет (нестандартные миграции), пропускаем молча.
                pass

    # Продавец: просмотр/добавление продаж + просмотр товаров/категорий
    for code in ["view_sale", "add_sale", "view_product", "view_category"]:
        if code in perms:
            seller_group.permissions.add(perms[code])

    # Админ магазина: всё из перечисленного
    for code in perms:
        admin_group.permissions.add(perms[code])

def ensure_users():
    # Создадим демо-пользователей, если их нет
    if not User.objects.filter(username="admin").exists():
        User.objects.create_superuser(username="admin", email="", password="admin")

    if not User.objects.filter(username="seller").exists():
        u = User.objects.create_user(username="seller", password="seller")
        grp = Group.objects.filter(name="seller").first()
        if grp:
            u.groups.add(grp)

def ensure_demo_data():
    """
    Создаёт несколько категорий и товаров, если база пуста.
    Возвращает словарь продуктов по SKU (для совместимости со старым кодом).
    """
    if Product.objects.exists():
        # Уже есть данные — возвращаем «индекс» по SKU
        return {p.sku: p for p in Product.objects.all()}

    # Категории
    printers, _ = Category.objects.get_or_create(name="Принтеры")
    paper, _ = Category.objects.get_or_create(name="Бумага")
    accessories, _ = Category.objects.get_or_create(name="Аксессуары")

    demo = [
        dict(sku="PRN-001", name="Лазерный принтер A4", price=12990, stock=5, category=printers),
        dict(sku="PRN-002", name="Струйный принтер A4", price=8990, stock=7, category=printers),
        dict(sku="PPR-500", name="Бумага А4, 500л", price=590, stock=40, category=paper),
        dict(sku="USB-010", name="Кабель USB-B 1м", price=290, stock=25, category=accessories),
    ]

    created = {}
    for row in demo:
        p, _ = Product.objects.get_or_create(
            sku=row["sku"],
            defaults={
                "name": row["name"],
                "price": row["price"],
                "stock": row["stock"],
                "category": row["category"],
                "is_active": True,
            },
        )
        created[p.sku] = p
    return created