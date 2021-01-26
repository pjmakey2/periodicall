from django_celery_beat.models import CrontabSchedule, PeriodicTask
from django.utils.timezone import now
import datetime
import json

schedule_one, _ = CrontabSchedule.objects.get_or_create(
     minute='27',
     hour='*',
     day_of_week='*',
     day_of_month='*',
     month_of_year='*',
 )

schedule_two, created = IntervalSchedule.objects.get_or_create(
     every=10,
     period=IntervalSchedule.SECONDS,
 )



from random import choice
quotes = "Not my circus, not my monkeys",\
         "Don't eat yellow snow",\
         "Never bring a sword to a gunfight",\
         "The truth is out there"
qtt = choice(quotes)
PeriodicTask.objects.create(
        crontab=schedule_one,
        name='This is Tree',
        task='task_manag.tasks.test_periodicall',
        args=json.dumps([qtt]),
        kwargs=json.dumps({}),
        expires=now() + datetime.timedelta(seconds=60*10)
)
qtt = choice(quotes)
PeriodicTask.objects.create(
        interval=schedule_two,
        name='This is Two',
        task='task_manag.tasks.test_periodicall',
        args=json.dumps([qtt]),
        kwargs=json.dumps({}),
        expires=now() + datetime.timedelta(seconds=60*5)
)

#####################To test the celery worker from ipython shell################
from celery.execute import send_task
 send_task('task_manag.tasks.test_periodicall', args=['hola mundo'], kwargs={})
