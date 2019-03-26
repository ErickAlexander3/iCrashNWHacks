from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField

'''
    Sprint Demo entries used for testing the sending of data from
    the de1 to the server through the WIFI chip
'''
class DemoEntries(models.Model):
    text = models.TextField()
    save_time = models.DateTimeField(auto_now_add=True)

'''
    An extension of the basic Django user, that includes any information given by the
    user and a JSON-formatted list of emergency contacts
'''
class UserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    emergency_service_provider = models.BooleanField(default=False)
    contacts = JSONField(default=list)

'''
    A representation of every physical device using their serial numbers
'''
class Device(models.Model):
    serial = models.TextField(unique=True)

'''
    A middleware class for the relationship between a user and some device, which includes
    the 4-digits PIN required for login
'''
class UserPin(models.Model):
    device = models.ForeignKey(Device, related_name="user_pin_entries", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pin = models.TextField(null=False)

'''
    The class representing the logs sent by all of the devices of a specific user. It also
    includes a public ID of the video of the recorded crash, which was uploaded to
    Cloudinary
'''
class CrashLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    log = JSONField()
    save_time = models.DateTimeField(auto_now_add=True)
    recorded_crash = models.TextField()