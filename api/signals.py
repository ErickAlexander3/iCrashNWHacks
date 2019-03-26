from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserInfo
from django.db.models import signals

from allauth.account.signals import user_signed_up
import pdb

'''
	On user registration, trigger a signal to create the user info class linked to that user
'''
@receiver(user_signed_up)
def post_user_creation_setup(sender, user, **kwargs):
    #pdb.set_trace()
    referer = kwargs["request"].META.get('HTTP_REFERER')
    emergency_service_provider = False
    if referer is not None and "emergency_service_provider=true" in referer:
        emergency_service_provider = True
    UserInfo.objects.create(user=user, emergency_service_provider=emergency_service_provider)