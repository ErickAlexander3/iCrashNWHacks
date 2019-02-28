from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField, HStoreField

class DemoEntries(models.Model):
    text = models.TextField()
    save_time = models.DateTimeField(auto_now_add=True)

class UserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    info = HStoreField(null=True)
    contacts = JSONField(default=list)

class Device(models.Model):
    serial = models.TextField(unique=True)

class UserPin(models.Model):
    device = models.ForeignKey(Device, related_name="user_pin_entries", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pin = models.TextField(null=False)


class CrashLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    log = JSONField()
    save_time = models.DateTimeField(auto_now_add=True)
    recorded_crash = models.TextField()