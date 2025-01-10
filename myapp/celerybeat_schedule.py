# celerybeat_schedule.py
# Schedule the task: Use Celery's periodic task feature to schedule the task to run daily at 8 AM. Add the following to your celery.py or a new celerybeat_schedule.py file.
from celery import app
from celery.schedules import crontab

app.conf.beat_schedule = {
    'send-daily-sales-report': {
        'task': 'home.tasks.send_daily_eqpt_report',
        'schedule': crontab(hour=10, minute=35),
    },
}