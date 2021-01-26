This is a test of the django-celery-beat packages

You will need.

#Python version.

 3+

# Python packages

  - django
  - django-celery-beat
  - celery
  - django-extensions

# Servers

  - Sqlite
  - Redis
  - Rabbitmq

# Initialize the database

```bash
  python manage.py migrate
```

# Initialize the worker and the beat
## Beat

```bash
celery -A periodicall beat -l debug --scheduler django_celery_beat.schedulers:DatabaseScheduler
```

## Worker

```bash
celery -A periodicall worker -l DEBUG
```

FYI: You have the possibility to run either the worker and the beat in one command, but I think for monitoring is more convenient to execute then separately

## Run a task periodically

### Open a django shell

```bash
  python manage shell_plus
```

### Paste this code and execute it

```python

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
```

In the terminals that's running the worker and the beat, you will see how the beat is listening for changes in the database and the worker receive the periodic task


## Test your worker directly

The next snippet is if you want to test if your worker works directly

```python
from celery.execute import send_task
send_task('task_manag.tasks.test_periodicall', args=['hola mundo'], kwargs={})

```
