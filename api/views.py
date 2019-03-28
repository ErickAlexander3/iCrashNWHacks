from django.shortcuts import render
from .models import DemoEntries, Device, UserPin, UserInfo, CrashLog
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from django.contrib.auth.models import User

from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .serializers import EmergencyContactsSerializer, CrashLogSerializer, CrashPointSerializer
from .permissions import EmergencyServicePermission
import pdb
import json

'''
    Used for our Sprint Demo to send crash information from the de1 to the server
'''
@require_http_methods(["POST",])
def demo(request):
    entry = DemoEntries()
    entry.text = request.body.decode('utf-8')
    entry.save()

    return HttpResponse(status=204)

'''
    Get a json-formatted list of users for a specific device
'''
def get_user_list(request):
    data = json.loads(request.body)
    serial = data.get("serial")
    users = []
    device = Device.objects.filter(serial=serial).first()
    if device:
        for user_pin in device.user_pin_entries.all():
            users.append(user_pin.user.username)

    return JsonResponse({"users": users})

'''
    Get a json-formatted list of emergency contacts for a specific user.
    Update: Due to the complexity of the parsing in our WIFI chip, we changed this to
    a comma-separated string
'''
def get_emergency_contacts(request):
    data = json.loads(request.body)
    username = data.get("user")
    contacts = ""
    user = User.objects.filter(username=username).first()
    if user:
        for contact in user.userinfo.contacts:
            contacts += contact["name"] + " " + contact["phone_number"] + ","

    if contacts.endswith(","):
        contacts = contacts[:-1]
    
    return HttpResponse(contacts)

'''
    Add a user to the list of users for a device, with a specific PIN for login
'''
@require_http_methods(["POST",])
@login_required
def add_device(request):
    serial = request.POST.get("serial")
    pin = request.POST.get("pin")
    device, created = Device.objects.get_or_create(serial=serial)
    #if new device created, or if a user-device relationship exists doesn't exist, create the new entry
    if created or not UserPin.objects.filter(device=device, user=request.user).exists():
        serial_pin_entry = UserPin(device=device, user=request.user, pin=pin)
        serial_pin_entry.save()
    
    return redirect("/")



'''
    Add an emergency contact to the list of contafts for a specific user
'''
@require_http_methods(["POST",])
@login_required
def add_emergency_contact(request):
    name = request.POST.get("name")
    phone_number = request.POST.get("phone_number")
    user_info = UserInfo.objects.filter(user=request.user).first()
    #if new device created, or if a user-device relationship exists doesn't exist, create the new entry
    if user_info:
        #pdb.set_trace()
        user_info.contacts.append({'name': name, 'phone_number': phone_number})
        user_info.save()
    
    return redirect("/")

'''
    Edit User Info to change the user's license plate
'''
@require_http_methods(["POST",])
@login_required
def edit_user_info(request):
    license_plate = request.POST.get("license_plate")
    user_info = UserInfo.objects.filter(user=request.user).first()
    pdb.set_trace()
    if user_info and license_plate:
        pdb.set_trace()
        user_info.license_plate = license_plate
        user_info.save()
    
    return redirect("/")

'''
    Authenticate the credentials of a user given a device and a login PIN.
    Note: This will not authenticate the user in the server, but it will tell
    our demo device whether those credentials are valid or not
'''
@require_http_methods(["POST",])
def login_device(request):
    data = json.loads(request.body)
    serial = data.get("serial")
    username = data.get("username")
    pin = data.get("pin")

    device = Device.objects.filter(serial=serial).first()
    user_pin_entry = UserPin.objects.filter(user__username=username, device=device).first()
    if user_pin_entry and user_pin_entry.pin == pin:
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=403)

'''
    After a crash, send the log to the server, including the public id for the video
    uploaded to Cloudinary
'''
@require_http_methods(["POST",])
def log_crash(request):
    #pdb.set_trace()
    data = json.loads(request.body)
    username = data.get("username")
    log = data.get("log")
    recorded_crash = data.get("crash_public_id")
    user = User.objects.filter(username=username).first()
    if user:
        new_log = CrashLog.objects.create(user=user, log=log, recorded_crash=recorded_crash)
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=400)




class EmergencyServiceViewSet(viewsets.ViewSet):
    #permission_classes = [IsAuthenticated, EmergencyServicePermission]

    def list(self, request):
        license_plate = request.GET.get('license_plate')
        if license_plate is None:
            return Response("Please enter a license plate",
                            status=status.HTTP_400_BAD_REQUEST)

        user_to_query = User.objects.filter(userinfo__license_plate=license_plate).first()
        if user_to_query is None:
            return Response("Not a valid license plate",
                            status=status.HTTP_400_BAD_REQUEST)

        emergency_contacts_serializer = EmergencyContactsSerializer(user_to_query.userinfo)
        crash_log_serializer = CrashLogSerializer(CrashLog.objects.filter(user=user_to_query), many=True)

        return Response(crash_log_serializer.data)

        """
        return Response({
            'crash_logs': crash_log_serializer.data,
            'emergency_contacts': emergency_contacts_serializer.data,
        })
        """

class CrashPointViewSet(viewsets.ViewSet):
    #permission_classes = [IsAuthenticated, EmergencyServicePermission]

    def list(self, request):
        queryset = CrashLog.objects.all()
        crash_points_serializer = CrashPointSerializer(queryset, many=True)

        return Response(crash_points_serializer.data)