from django.shortcuts import render

# Create your views here.

import pdb
def home(request):
	return render(request, 'home.html')