from rest_framework import serializers
from .models import CrashLog, UserInfo
from django.contrib.auth.models import User

class EmergencyContactsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        fields = ('contacts',)

class CrashLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrashLog
        fields = ('log', 'save_time', 'recorded_crash')