# Notifications REST API Template for PlutoFramework

### .env example:
```dotenv
# App setup
DEBUG="0"
DJANGO_ALLOWED_HOSTS=".onrender.com"
SECRET_KEY="*******"
GOOGLE_APPLICATION_CREDENTIALS_JSON='{"type": "service_account","project_id": ... '

# Database setup
PG_URL="*******"
PG_DATABASE="railway"
PG_HOST="*******"
PG_PASSWORD="*******"
PG_PORT="33911"
PG_USER="postgres"
```

### Run
#### Development:
```shell
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```
> [!NOTE]  
> If DEBUG is off, you will still have to collect static

#### Production:
```shell
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic
gunicorn ApiCore.wsgi:application --bind 0.0.0.0:$PORT
```

> [!NOTE]  
> `$PORT` environment variable should be supplied by hosting platform