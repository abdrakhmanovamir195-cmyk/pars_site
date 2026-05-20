import os


class Celery:
    pass


from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scraper.settings')
app = Celery('scraper')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


def shared_task():
    return None