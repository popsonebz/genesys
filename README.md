# User Management System

## Pre-requisite

1. Install python 3.7.5

2. Install requirements
```
pip install -R requirements.txt
```

3. Run Database Migration
```
python manage.py makemigrations 'user_management'
python manage.py migrate
```

4. Create Admin user
```
python manage.py createsuperuser
```

5. Run Server
```
python manage.py runserver 0.0.0.0:8001
```

6. Visit Swagger doc on the browser for endpoints

```
localhost:8001
```
