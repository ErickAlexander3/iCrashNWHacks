from django.shortcuts import render
from .models import DemoEntries
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
@require_http_methods(["POST",])
def demo(request):
	entry = DemoEntries()
	entry.text = request.body.decode('utf-8')
	entry.save()

	return HttpResponse(status=204)