# Notifications REST API Template for PlutoFramework

## URLs
```
GET /admin - All admin tools needed (including login)
POST /api/nonce - Generate the nonce (needed for app integrity attestation)
POST /api/token - Register device to get JWT pair
POST /api/token/refresh - Refresh access token using refresh token
POST /api/fcm/token-update - Update the FCM token
```
## Setup
### 1. Database
Set up a database on a remote server and get access credentials, then put them in .env file.

### 2. Firebase
In the Firebase console, open Settings > Service Accounts.
Click Generate New Private Key, then confirm by clicking Generate Key.
Securely store that JSON file.

### 3. Google Integrity API
Set up the project (including Play Console and Google Cloud).
Turn on Integrity API in Console settings.
Then change response encryption to manual and get the Decryption and Verification keys.

### .env example:
```dotenv
# App setup
DEBUG=0
DJANGO_ALLOWED_HOSTS=".onrender.com,0.0.0.0"
SECRET_KEY="***"
FIREBASE_CREDENTIALS_JSON='{
  "type": "service_account",
  "project_id": "...",
  "private_key_id": "...",
  "private_key": "-----BEGIN PRIVATE KEY-----...-----END PRIVATE KEY-----\n",
  "client_email": "...",
  "client_id": "...",
  "auth_uri": "https://accounts.google.com...",
  "token_uri": "https://oauth2.googleapis.com...",
  "auth_provider_x509_cert_url": "https://www.googleapis.com...",
  "client_x509_cert_url": "https://www.googleapis.com...",
  "universe_domain": "googleapis.com"
}'

# App attestation
APK_NAME="com.companyname.appname"
ATTESTATION_DECRYPTION_KEY="***"
ATTESTATION_VERIFICATION_KEY="***"
ATTESTATION_APP_SIGNING_KEY="XX:XX:XX:XX:XX:XX..."

# Database setup
PG_URL="postgresql://..."
PG_DATABASE="db_name"
PG_HOST="some.url.com"
PG_PASSWORD="***"
PG_PORT="5432"
PG_USER="admin"
```

### Install libraries
```shell
pip install -r requirements.txt
```
### Prepare the database
```shell
python manage.py migrate
```

### Add a superuser to access API as admin (optional)
```shell
python manage.py createsuperuser
```

## Run
#### Development:
```shell
python manage.py runserver
```
> [!NOTE]  
> If DEBUG is off, you will have to collect static like in production

#### Production:
```shell
python manage.py collectstatic
gunicorn ApiCore.wsgi:application --bind 0.0.0.0:$PORT
```

> [!NOTE]  
> `$PORT` environment variable should be supplied by hosting platform