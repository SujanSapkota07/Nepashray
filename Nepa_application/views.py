# from math import sumprod
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth import views as auth_views
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
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



def get_total_comments_for_user(username):
    # Get the user object by username
    user = User.objects.get(username=username)

    # Now you can use this user object to retrieve the total comments
    total_comments = models.Comment.objects.filter(author=user).count()

    return total_comments



def discover(request):
    categories = models.Category.objects.all()
    return render(request, 'discovernew.html',{"categories": categories})


def category_clicked(request, category=None):
    categoryObj = models.Category.objects.get(name=category)
    categoryTopic = categoryObj.topics.all()
    return render(request, 'listofpost.html', context={"posts":categoryTopic})

def provience_clicked(request, province=None): 
    provinceObj = models.province.objects.get(name=province)
    provinceTopic = provinceObj.topics.all()
    return render(request, 'listofpost.html', context={"posts":provinceTopic})

def search(request):
    return render(request, 'discoverr.html')


def index(request): # for landing page 
    provinces = province.objects.all()
    username = None
    # providing the topic of latest three post 
    latest_posts =models.Topic.objects.prefetch_related('t_image_set').all()[:3]
    if request.user.is_authenticated:
        username = request.user.username
    context = {
        "provinces": provinces,
        "username": username,
        "latest_posts": latest_posts,
    }
    return render(request, 'index.html', context)



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
    # get the username of the user
    username = request.user.username
    if request.method == 'POST':

        form = forms.TopicForm(request.POST, request.FILES) 
        if form.is_valid():
            topic = form.save(commit=False)
            topic.author = username
            models.Topic.is_verified = False
            category_ids = request.POST.getlist('category')
            topic.save()
            topic.category.add(*category_ids)
            for image in request.FILES.getlist('images'):
                models.T_Image.objects.create(topic=topic, image=image)
            print("-----------Post created successfully-----------")
            return redirect('listofpost')
    else:
        form = forms.TopicForm()
    return render(request, 'create_topic.html', {'form': form, 'username':username})


# this code is removed after dashboard is created
# def create(request):
#     return render(request, 'create.html') # has to be added

def listofpost(request):
    # Retrieve all topics with related T_Image instances
    posts = models.Topic.objects.prefetch_related('t_image_set').all()
    user = request.user.username
    context = {
        "posts": posts,
        "user": user,
        }
    return render(request, 'listofpost.html', context)

# function to calculate total views got by user in all post
def views(username):
    posts = models.Topic.objects.filter(author=username)
    total_views = 0
    for post in posts:
        total_views += post.views
    return total_views


@login_required(login_url="authsignin")
def upload(request):
    context = []
    username = request.user.username
    total_likess = views(username)
    print(total_likess)
    if request.user.is_authenticated and  request.user.is_staff:
        unverified_posts = models.Topic.objects.filter(is_verified=False)
        categories = models.Category.objects.all()
        number_of_total_posts = models.Topic.objects.filter(is_verified=True).count()
        total_comments = get_total_comments_for_user(username)


        context = {'unverified_posts': unverified_posts,
                'username':username,
                'categories':categories,
                'number_of_total_posts':number_of_total_posts,
                'number':total_comments,
                'total_likes':total_likess,

                } 
    if request.user.is_authenticated and not request.user.is_staff:
        my_posts = models.Topic.objects.filter(author=username)
        date_created = models.Topic.objects.filter(author=username).values('post_date') 
        categories = models.Category.objects.filter(topics__in=my_posts)
        number_of_total_posts = my_posts.count()
        total_comments = get_total_comments_for_user(username)
        context = {'my_post': my_posts,
                'username':username,
                'categories':categories,
                'number_of_total_posts':number_of_total_posts,
                'date_created': date_created,
                'number':total_comments,
                'total_likes':total_likess,
                }
    return render(request, 'auth/admin_index.html', context)

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

def view_post(request, topic_id=None):
    topic = get_object_or_404(models.Topic, pk=topic_id)
    images = models.T_Image.objects.filter(topic=topic)
    user = request.user.username
    posts = models.Topic.objects.prefetch_related('t_image_set').all()

    context = {
        "topic": topic,
        "images": images,
        "posts": posts,
        "user": user,
    }
    return render(request, 'detailed_view.html', context)


def admin_contacts(request):
    contacts = models.Contact_us.objects.all()
    name = contacts.values('name')
    email = contacts.values('email')
    phone = contacts.values('phone')
    text_message = contacts.values('text_message')
    context = {
        "contacts": contacts,
        "name": name,
        "email": email,
        "phone": phone,
        "text_message": text_message,
    }

    return render(request, 'admin_contacts.html', context)



def manage_user(request):
    users = User.objects.filter(is_staff=False)
    # number=get_total_comments_for_user(users)
    print(users)
    context = {
        "users": users,
        # "number": number,
    }

    return render(request, 'manage_user.html', context)

def delete_user(request, user_id=None):
    user = get_object_or_404(User, pk=user_id)
    user.delete()
    return redirect('manage_user')


#detailed view of the post
def detailed_view(request, topic_id=None):
    topic = get_object_or_404(models.Topic, pk=topic_id)
    images = models.T_Image.objects.filter(topic=topic)
    user = request.user.username
    posts = models.Topic.objects.prefetch_related('t_image_set').all()
    likes = topic.likes.count()
    comments = models.Comment.objects.filter(post=topic)
    topic.views = topic.views + 1
    topic.save()


    context = {
        "topic": topic,
        "images": images,
        "posts": posts,
        "user": user,
        "likes": likes,
        "comments": comments,
    }
    return render(request, 'detailed_view.html', context)


@login_required
def report (request, topic_id=None):
    YOUR_THRESHOLD_VALUE = 1
    topic = get_object_or_404(models.Topic, pk=topic_id)

    if models.Report_Post.objects.filter(topic=topic, user=request.user).exists():
        print("-----------User has already reported this post-----------")
        return redirect('listofpost')
    else:
        # Increment the report count for the post
        topic.report = topic.report + 1

        # Save the report and associate it with the current user
        models.Report_Post.objects.create(topic=topic, user=request.user)

        # Check if the report count has reached the threshold to mark the post as unverified
        if topic.report >= YOUR_THRESHOLD_VALUE:
            topic.is_verified = False
            topic.save()
            print("-----------Post marked as unverified-----------")
            return redirect('index')
        else:
            print("-----------Post report is verified-----------")
            return redirect('listofpost')
    return redirect('detailed_view', topic_id=topic_id)



# @login_required
# def like_post(request, post_id):
#     post = get_object_or_404(models.Topic, pk=post_id)
#     post.likes.add(request.user)
#     return redirect('detailed_view', post_id=post_id)

# @login_required
# def unlike_post(request, post_id):
#     post = get_object_or_404(models.Topic, pk=post_id)
#     post.likes.remove(request.user)
#     return redirect('detailed_view', post_id=post_id)


# #like the post
# def like_post(request, topic_id=None):
#     print("-----------like added-----------")
#     topic = get_object_or_404(models.Topic, pk=topic_id)
#     topic.likes.add(request.user)
#     # like_text = "Unlike"
#     print("-------------like added-------------")
#     # like_count = topic.likes.count()
#     return render('detailed_view')

# def unlike_post(request, topic_id=None):
#     print("-----------like removed-----------")
#     topic = get_object_or_404(models.Topic, pk=topic_id)
#     topic.likes.remove(request.user)
#     # like_text = "Like"
#     print("-------------like removed-------------")
#     # like_count = topic.likes.count()
#     return render('detailed_view')



@login_required(login_url="authsignin")
def add_comment(request, id=None):
   if request.method == "POST":
       try:
           content = request.POST.get("comment-content")
           post = models.Topic.objects.get(id=id)
           models.Comment.objects.create(author=request.user, content=content, post=post)
           post.commentCount += 1
           post.save()
       except Exception as e:
           return HttpResponse(e)
   return HttpResponseRedirect(reverse("detailed_view", args=[id]))

