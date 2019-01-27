from django.db import models
from django.db.models import BooleanField
from django.db.models import DateTimeField
from django.db.models import FloatField
from django.conf import settings
from django.urls import reverse
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from django.contrib.auth import models as auth_models
from datetime import datetime as datetime

class ParkingSession(models.Model):

    # Fields
    plateNo = models.CharField(max_length = 6, null = True)
    startTime = models.DateTimeField()
    endTime = models.DateTimeField(null = True)
    price = models.FloatField(default = 10, verbose_name = "Hourly rate")
    isLegalSession = models.BooleanField()