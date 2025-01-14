from django.core.management.base import BaseCommand
from celery import current_app
from celery.beat import Service

class Command(BaseCommand):
    help = 'Check the Celery Beat schedule'

    def handle(self, *args, **kwargs):
        app = current_app._get_current_object()
        service = Service(app)
        schedule = service.get_scheduler().get_schedule()

        for task_name, task in schedule.items():
            self.stdout.write(f"Task: {task_name}, Next Run Time: {task.schedule}")