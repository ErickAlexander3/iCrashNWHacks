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

class Customer(models.Model):


    # Relationship Fields
    customerInformation = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, primary_key = True
    )

class Manager(models.Model):


    # Relationship Fields
    managerInformation = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, primary_key = True
    )

class ParkingStall(models.Model):

    # Fields
    availability = models.BooleanField(default = False)
    price = models.FloatField(default = 10, verbose_name = "Hourly rate")

    # Relationship Fields
    managerInformation = models.ForeignKey(
        'api.Manager',
        on_delete=models.CASCADE, related_name="managers", primary_key = True
    )

class ParkingSession(models.Model):

    # Fields
    startTime = models.DateTimeField(default = datetime.now())
    endTime = models.DateTimeField(blank = True)
    cost = models.FloatField()
    hasPaid = models.BooleanField(default = False)
    isLegalSession = models.BooleanField()

    # Relationship Fields
    parkingStall = models.ForeignKey(
        'api.ParkingStall',
        on_delete=models.CASCADE
    )
    customerInformation = models.ForeignKey(
        'api.Customer',
        on_delete=models.CASCADE
    )