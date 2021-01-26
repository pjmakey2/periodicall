from django.db import models

# Create your models here.


class Response(models.Model):
    time = models.DateTimeField()
    message = models.CharField(max_length=80)
