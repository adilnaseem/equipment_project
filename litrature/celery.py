# type: ignore
To use Celery with your Django project you must first define an instance of the Celery library (called an “app”)

If you have a modern Django project layout like:

- proj/
  - manage.py
  - proj/
    - __init__.py
    - settings.py
    - urls.py

then the recommended way is to create a new proj/proj/celery.py module that defines the Celery instance:
#---------- file:  proj/proj/celery.py---------start
import os

from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proj.settings')

app = Celery('proj')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')

#---------- file:  proj/proj/celery.py---------end

Then you need to import this app in your proj/proj/__init__.py module. This ensures that the app is loaded when Django starts so that the @shared_task decorator (mentioned later) will use it:

proj/proj/__init__.py:

# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.
from .celery import app as celery_app

__all__ = ('celery_app',)