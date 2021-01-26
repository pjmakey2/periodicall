from celery import shared_task
from task_manag.models import Response
import datetime

@shared_task
def test_periodicall(msg):
    now = datetime.datetime.now()
    Response.objects.create(
        time = now,
        message = msg
    )
    return {'success': 'Store at {}'.format(now.strftime('%Y%m%d %H%M%S'))}

