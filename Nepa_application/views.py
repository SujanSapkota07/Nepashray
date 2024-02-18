from django.shortcuts import render, redirect
from .models import province
from . import models
from django.contrib import messages
from . import forms
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404


# Create your views here.

# def index(request):
#     provience_dic = provience.objects.all()
#     return render(request, 'index.html')

# def contact_us(request):
#     return render(request, 'contactpage.html')

def register(request):
    return render(request, 'auth/landingpage.html')


def discover(request):
    categories = models.Category.objects.all()
    return render(request, 'discovernew.html',{"categories": categories})

def category_clicked(request, category=None):
    categoryObj = models.Category.objects.get(name=category)
    categoryTopic = categoryObj.topics.all()
    return render(request, 'genre_landingpage.html', context={"posts":categoryTopic})


def search(request):
    return render(request, 'discoverr.html')


def index(request): # for landing page 
    provinces = province.objects.all()
    username = None
    if request.user.is_authenticated:
        username = request.user.username
    return render(request, 'index.html', {'provinces': provinces, 'username':username} )


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


@login_required
def create_topic(request):
    username = None
    username = request.user.username
    if request.method == 'POST':

        form = forms.TopicForm(request.POST, request.FILES) 
        if form.is_valid():
            topic = form.save(commit=False)
            models.Topic.is_verified = False
            topic.author = username
            topic.save()
            for image in request.FILES.getlist('images'):
                models.T_Image.objects.create(topic=topic, image=image)
            return redirect('listofpost')
    else:
        form = forms.TopicForm()
    return render(request, 'create_topic.html', {'form': form, 'username':username})


# def create(request):
#     return render(request, 'create.html') # has to be added

def listofpost(request):
    # Retrieve all topics with related T_Image instances
    posts = models.Topic.objects.prefetch_related('t_image_set').all()
    return render(request, 'listofpost.html', {"posts": posts})


@login_required
def upload(request):
    contex = []
    username = request.user.username
    unverified_posts = models.Topic.objects.filter(is_verified=False)
    categories = models.Category.objects.all()
    contex = {'unverified_posts': unverified_posts, 'username':username, 'categories':categories} # make changes here
    return render(request, 'auth/admin_index.html', contex)

# verification of the post
def verify_post(request, topic_id=None):
    print(1)
    topic = get_object_or_404(models.Topic, pk=topic_id)
    print(2)
    if not topic.is_verified: # Check if the post is not already verified
        topic.is_verified = True  # Verify the post
        topic.save()
        print(3)

    return redirect('upload')# make changes here

# blocking of the post
def block_post(request, topic_id=None):
    topic = get_object_or_404(models.Topic, pk=topic_id)
    topic.delete()
    return redirect('upload')# make changes here