from django.shortcuts import render, redirect
from .models import province
from . import models
from django.contrib import messages
from . import forms


# Create your views here.

# def index(request):
#     provience_dic = provience.objects.all()
#     return render(request, 'index.html')

# def contact_us(request):
#     return render(request, 'contactpage.html')

def register(request):
    return render(request, 'register.html')


def discover(request):
    categories = models.Category.objects.all()
    print(categories)
    return render(request, 'discovernew.html',{"categories": categories})

def category_clicked(request, category=None):
    categoryObj = models.Category.objects.get(name=category)
    categoryTopic = categoryObj.topics.all()
    return render(request, 'genre_landingpage.html', context={"posts":categoryTopic})


def search(request):
    return render(request, 'discoverr.html')


def index(request): # for landing page 
    provinces = province.objects.all()
    # context = {'provinces': proviences}
    return render(request, 'index.html', {'provinces': provinces} )


def provience_clicked(request, province=None): 
    provinceObj = models.province.objects.get(name=province)
    provinceTopic = provinceObj.topics.all()
    return render(request, 'province_landingpage.html', context={"posts":provinceTopic})

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
            return render(request, 'listofpost.html')
    else:


        form = forms.TopicForm()
    return render(request, 'create_topic.html', {'form': form})


def create(request):
    return render(request, 'create.html') # has to be added

def listofpost(request):
    # Retrieve all topics with related T_Image instances
    posts = models.Topic.objects.prefetch_related('t_image_set').all()
    return render(request, 'listofpost.html', {"posts": posts})