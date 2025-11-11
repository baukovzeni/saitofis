 py -m venv .venv

.\.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python manage.py migrate



 python manage.py runserver

daphne -b 127.0.0.1 -p 8000 taxi_dispatch.asgi:application