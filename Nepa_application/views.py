from django.shortcuts import render
from .models import provience

# Create your views here.

def index(request):
    provience_dic = provience.objects.all()
    return render(request, 'index.html')

def contact_us(request):
    return render(request, 'contactpage.html')

def register(request):
    return render(request, 'register.html')

def discover(request):
    return render(request, 'discovernew.html')

def search(request):
    return render(request, 'discoverr.html')