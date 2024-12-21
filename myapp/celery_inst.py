# type: ignore
how to use celery in django? 


Using Celery with Django involves several steps. Celery is an asynchronous task queue/job queue based on distributed message passing. It is used to run time-consuming tasks in the background and is particularly useful for tasks that you don't want to block your web server from responding to requests.

Here’s a step-by-step guide to integrating Celery into a Django project:

Step 1: Install Required Packages
First, you need to install Celery and a message broker. RabbitMQ and Redis are two popular choices for brokers. For this example, we'll use Redis.


pip install celery redis
Step 2: Configure Celery in Your Django Project
Create a new file named celery.py in your Django project directory (the same directory as settings.py).


# myproject/celery.py

import os
from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

app = Celery('myproject')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()
Next, update your __init__.py file in the same directory to ensure the Celery app is loaded when Django starts.


# myproject/__init__.py

from .celery import app as celery_app

__all__ = ('celery_app',)
Step 3: Configure Celery Settings in Django
Add the following configuration to your settings.py file.


# myproject/settings.py

# Celery Configuration
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
Make sure you have Redis running on your machine or adjust the CELERY_BROKER_URL and CELERY_RESULT_BACKEND to point to your Redis server.

Step 4: Create a Celery Task
Create a new file named tasks.py inside one of your Django apps.


# myapp/tasks.py

from celery import shared_task

@shared_task
def add(x, y):
    return x + y
Step 5: Run Celery Worker
Open a terminal and navigate to your Django project directory. Then, run the Celery worker.


celery -A myproject worker --loglevel=info
celery -A myapp worker -l info
Step 6: Call the Celery Task
You can now call the Celery task from anywhere in your Django code. For example, in a view:


# myapp/views.py

from django.http import JsonResponse
from .tasks import add

def trigger_task(request):
    result = add.delay(4, 4)
    return JsonResponse({'task_id': result.id})
Step 7: Check Task Status (Optional)
If you want to check the status of a task, you can do so using the task ID returned when you called the task.


# myapp/views.py

from django.http import JsonResponse
from celery.result import AsyncResult
from .tasks import add

def get_task_status(request, task_id):
    result = AsyncResult(task_id)
    response_data = {
        'task_id': task_id,
        'status': result.status,
        'result': result.result if result.ready() else None
    }
    return JsonResponse(response_data)
Conclusion
This is a basic setup to get you started with Celery in a Django project. Depending on your needs, you might want to explore more advanced features like periodic tasks, custom task routing, and more.