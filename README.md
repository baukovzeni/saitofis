# Сайтофис POS (Auto-setup v2)
✔ Добавлены **миграции** для apps (products, customers, sales)
✔ `post_migrate` ждёт создания таблиц и только потом заливает демо-данные/дизайн/пользователей

## Старт
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python manage.py migrate    # авто-заполнение произойдёт безопасно
python manage.py runserver
```
Логины: admin/admin12345, seller/seller123
