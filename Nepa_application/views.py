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
from django.core.mail import send_mail


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

# function to calculate total comments got by user in all post
def comments(username):
    posts = models.Topic.objects.filter(author=username)
    total_comments = 0
    for post in posts:
        total_comments += post.commentCount
    return total_comments


@login_required(login_url="authsignin")
def upload(request):
    context = []
    username = request.user.username
    total_likess = views(username)
    total_comments = comments(username)
    if request.user.is_authenticated and  request.user.is_staff:
        unverified_posts = models.Topic.objects.filter(is_verified=False)
        categories = models.Category.objects.all()
        number_of_total_posts = models.Topic.objects.filter(is_verified=True).count()
        # total_comments = get_total_comments_for_user(username)
        # total_comments = comments(username)


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
        # total_comments = get_total_comments_for_user(username)
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
    # users = User.objects.all()
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

    if request.user in topic.likes.all():
        liked = True
    else:
        liked = False
    comments = models.Comment.objects.filter(post=topic)
    topic.views = topic.views + 1
    topic.save()


    context = {
        "topic": topic,
        "images": images,
        "posts": posts,
        "user": user,
        "liked": liked,
        "comments": comments,
        "likes": likes,
    }
    return render(request, 'detailed_view.html', context)


@login_required
def report (request, topic_id=None):
    YOUR_THRESHOLD_VALUE = 1
    topic = get_object_or_404(models.Topic, pk=topic_id)

    if models.Report_Post.objects.filter(topic=topic, user=request.user).exists():
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
            return redirect('index')
        else:
            return redirect('listofpost')
    return redirect('detailed_view', topic_id=topic_id)


# like the post
@login_required
def like_post(request, topic_id):
     
    topic = get_object_or_404(models.Topic, pk=topic_id)
    images = models.T_Image.objects.filter(topic=topic)
    user = request.user.username
    posts = models.Topic.objects.prefetch_related('t_image_set').all()
    likes = topic.likes.count()
    topic.likes.add(request.user)

    if request.user in topic.likes.all():
        liked = True
    else:
        liked = False
    comments = models.Comment.objects.filter(post=topic)
    topic.save()


    context = {
        "topic": topic,
        "images": images,
        "posts": posts,
        "user": user,
        "liked": liked,
        "comments": comments,
        "likes": likes,
    }
    return render(request, 'detailed_view.html', context)



# unlike the post
@login_required
def unlike_post(request, topic_id):
    
    topic = get_object_or_404(models.Topic, pk=topic_id)
    images = models.T_Image.objects.filter(topic=topic)
    user = request.user.username
    posts = models.Topic.objects.prefetch_related('t_image_set').all()
    likes = topic.likes.count()
    topic.likes.remove(request.user)

    if request.user in topic.likes.all():
        liked = True
    else:
        liked = False
    comments = models.Comment.objects.filter(post=topic)
    topic.save()


    context = {
        "topic": topic,
        "images": images,
        "posts": posts,
        "user": user,
        "liked": liked,
        "comments": comments,
        "likes": likes,
    }
    return render(request, 'detailed_view.html', context)




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

# function to search the contents
def search_view(request):
    query = request.GET.get('q')
    results = []
    user = request.user.username

    if query:

        #Search for users
        user_topics = models.Topic.objects.filter(author__icontains=query).order_by('post_date')
        results.extend(user_topics)
        # Search for topics
        topics = models.Topic.objects.filter(title__icontains=query)
        results.extend(topics)

        # Search for provinces
        provinces = province.objects.filter(name__icontains=query)
        for provincee in provinces:
            province_topics = provincee.topics.all()
            results.extend(province_topics)

        # Search for categories
        categories = models.Category.objects.filter(name__icontains=query)
        for category in categories:
            category_topics = category.topics.all()
            results.extend(category_topics)


        unique_results=list(set(results))
        results = sorted(unique_results, key=lambda x: x.post_date, reverse=True)

    context = {
        'query': query,
        'posts': results,
        # 'posts': unique_results,
        'user': user
    }
    return render(request, 'listofpost.html', context)

def contact_author(request):
    # sender_email = models.Message.objects.values('sender_email')
    # receiver_email = models.Message.objects.values('receiver_email')
    # text_message = models.Message.objects.values('text_message')
    # context = {
    #     "sender_email": sender_email,
    #     "receiver_email": receiver_email,
    #     "text_message": text_message,
    # }
    messages = models.Message.objects.all()
    context={
        "messages": messages,
    }
    return render(request, 'contact_author.html', context)

def toauthor(request, topic_id=None):
   if request.method == 'POST':
        text_message = request.POST.get('message', '')
        user = request.user
        sender_email = user.email # my email
        topic = models.Topic.objects.get(id=topic_id)
        author = topic.author
        receiver_email = User.objects.get(username=author).email # author email
         # Create and save the Message instance
        message = models.Message(
            sender_email=sender_email,
            receiver_email=receiver_email,
            text_message=text_message,
        )
        message.save()
        # currently showing emails of sender and receiver, later make it show username

        return HttpResponse('Message sent, Please return to the previous page to continue browsing')
   else:
       return HttpResponse('Message not sent')

def delete_email(request,message_id=None):
    message = get_object_or_404(models.Message, pk=message_id)
    # get the username of sender
    username = User.objects.get(email=message.sender_email).username
    print(username)
    message.delete()
    return redirect('contact_author')

def approve_email(request,message_id=None):
    message = get_object_or_404(models.Message, pk=message_id)
    username = User.objects.get(email=message.sender_email).username
    sender_email=message.sender_email
    receiver_email=message.receiver_email
    text_message=message.text_message
    # get the username of sender
    user = User.objects.get(email=sender_email)
    # send email to the author
    send_mail(
        "A user from Nepashraya has sent you a message",
        text_message+" \n\n\nThis email of the sender is : "+ sender_email+"\n\nThe username is: "+username,
        "project.nepashraya@gmail.com",
        [receiver_email],
        fail_silently=False,
        )
    message.delete()
    return redirect('contact_author')