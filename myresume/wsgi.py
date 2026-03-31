import os
import sys

# project path
project_home = "/home/sajjadan/repositories/myresume"

# add to python path
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# set settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myresume.settings")

# start django
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
