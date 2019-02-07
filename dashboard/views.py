from django.shortcuts import render
from api.models import DemoEntries

# Create your views here.

def home(request):
	return render(request, 'home.html', {'demo_entries': DemoEntries.objects.all()})