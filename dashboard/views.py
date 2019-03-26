from django.shortcuts import render
from api.models import DemoEntries
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods

from api.models import DemoEntries, Device, UserPin, UserInfo, CrashLog

import pdb

"""
	Return the landing page if not authenticated, or the dashboard if authenticated
"""
def home(request):
    if request.user.is_authenticated:
        user_pins = UserPin.objects.filter(user=request.user)
        user_info = UserInfo.objects.filter(user=request.user).first()
        crash_logs = CrashLog.objects.filter(user=request.user)
        if user_info.emergency_service_provider:
            return render(request, 'dashboard_emergency.html')

        return render(request, 'dashboard.html', {'user_pins': user_pins, 'user_info': user_info, 'crash_logs': crash_logs})
    else:
        return render(request, 'home.html', {'demo_entries': DemoEntries.objects.all()})


