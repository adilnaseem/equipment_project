# Create your tasks here

# from demoapp.models import Widget

from celery import shared_task

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