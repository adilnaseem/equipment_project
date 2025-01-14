# myapp/tasks.py
"""
celery -A myapp worker --loglevel=info    OR    celery -A myapp worker --pool=solo -l info
celery -A myapp beat --loglevel=info
"""
from celery import shared_task
from django.core.mail import send_mail
from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone
from . import models
# import models
@shared_task
def send_daily_eqpt_report():
    today = timezone.now().date()
    sold_count =models.Equipment.objects.filter().count()
    send_mail(
        'Daily Equipment Report',
        f'Total baggage x-ray machines today: {sold_count}',
        'adilnaseem.pak@gmail.com',
        ['adilnaseempk@yahoo.com'],
        fail_silently=False,
    )

@shared_task
def send_email_task(subject, message, from_email, recipient_list):
    send_mail(
        subject,
        message,
        from_email,
        recipient_list,
        fail_silently=False,
    )
@shared_task
def add(x, y):
    return x + y

@shared_task
def mul(x, y):
    return x * y

@shared_task
def xsum(numbers):
    return sum(numbers)
