import os
import sys
import django

# set settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myresume.settings")

# start django
django.setup()

from django.contrib.auth.models import User

username = "anik24"
email = "sa.anik24@gmail.com"
password = "Anik2019"

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print(f"Superuser '{username}' created successfully.")
    print(f"Username: {username}")
    print(f"Password: {password}")
else:
    print(f"Superuser '{username}' already exists.")
