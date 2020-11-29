#!/bin/bash

python manage.py shell -c "from environs import Env; \
                           env = Env(); \
                           env.read_env(); \
                           from user_management.models import User; \
                           User.objects.filter(email=env.str('ADMIN_EMAIL')).exists() or \
                           User.objects.create_superuser(env.str('ADMIN_EMAIL'), env.str('ADMIN_PASSWORD'))"
