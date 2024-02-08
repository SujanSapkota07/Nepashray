from django.shortcuts import render, redirect
from .models import provience
from django.contrib import messages
from . import forms
from django.contrib.auth import authenticate, login

# Create your views here.

# def index(request):
#     provience_dic = provience.objects.all()
#     return render(request, 'index.html')

# def contact_us(request):
#     return render(request, 'contactpage.html')

def register(request):
    return render(request, 'register.html')


def discover(request):
    return render(request, 'discovernew.html')


def search(request):
    return render(request, 'discoverr.html')


def index(request): # for landing page 
    proviences = provience.objects.all()
    # context = {'provinces': proviences}
    return render(request, 'index.html', {'provinces': proviences} )


def provience_clicked(request): 
    return render(request, 'province_landingpage.html' )


def contact_us(request):
    if request.method == 'POST':
        form = forms.contact(request.POST)
        if form.is_valid():
            contact_entry = form.save()
            return redirect('index')  # Assuming 'index' is the name of your index.html URL
        else:
            messages.error(request, "the form is not valid")
            return render(request, 'contactpage.html', {'form': form})
    else:
        form = forms.contact()
    return render(request, 'contactpage.html', {'form': form})

