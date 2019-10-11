from celery import shared_task
from django.db.models import F

from pages.models import Content


@shared_task
def increment_counter(content_id):
    content = Content.objects.filter(pk=content_id).first()
    if not content:
        return
    content.counter = F('counter') + 1
    content.save(update_fields=('counter',))
