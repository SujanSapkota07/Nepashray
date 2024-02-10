from django.shortcuts import render, redirect
from .models import provience
from . import models
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

# this fuction will let user to send messages to us
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


# let user post something
def create_topic(request):
    if request.method == 'POST':
        form = forms.TopicForm(request.POST, request.FILES)
        if form.is_valid():
            topic = form.save()
           
            for image in request.FILES.getlist('images'):
                models.T_Image.objects.create(topic=topic, image=image)
            return redirect('topic_detail', pk=topic.pk)
    else:
        form = forms.TopicForm()
    return render(request, 'create_topic.html', {'form': form})


def create(request):
    return render(request, 'create.html') # has to be added
