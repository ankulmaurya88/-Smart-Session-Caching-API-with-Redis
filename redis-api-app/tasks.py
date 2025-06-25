### redis-api-app/tasks.py
from celery import Celery

celery = Celery('tasks', broker='redis://localhost:6379/0')

@celery.task
def send_email(email):
    print(f"[Background Task] Sending email to {email}")
