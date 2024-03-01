from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from Nepa_Project import settings
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from . tokens import generate_token
from django.core.mail import EmailMessage, send_mail
from django.utils.encoding import force_str as force_text

# Create your views here.

# yeha uchit ko view huna parney, aba mero aauxa

def landingpage(request):
    return render(request, 'auth/landingpage.html')



def signup(request):
    if request.method == "POST":
       username = request.POST['username']
       fname = request.POST['fname']
       lname = request.POST['lname']
       email = request.POST['email']
       pass1 = request.POST['pass1']
       pass2 = request.POST['pass2']
    
       if User.objects.filter(username=username):
           messages.error(request, "Username already exists! Please try some other usernames")
           return redirect('authregister')
       
       
       if User.objects.filter(email=email):
           messages.error(request, "Email already registered!")
           return redirect('authregister')
       
       if len(username)>10:
           messages.error(request, "Username must be under 10 characters.")
       
       if pass1 != pass2:
           messages.error(request, "Passwords didnt match")
        
       if not username.isalnum():
           messages.error(request, "Username must be alphanumeric")
           return redirect('authregister')
       
       myuser = User.objects.create_user(username, email, pass1)
       myuser.first_name = fname
       myuser.last_name = lname
       myuser.is_active = False

       myuser.save()
       print(1)

       
       messages.success(request, "Your account has been successfully created! We have sent you a confirmation email, please confirm in order to activate your account")

       #Welcome email

       subject = "Registration on Nepashraya"
       message = "hello" + " "+ myuser.first_name + "!! \n" + "Welcome to NEPआश्रय!! \n  Thank you for visiting our website \n \n\n Thank you!\nNEPआश्रय Dev Team "
       from_email = settings.EMAIL_HOST_USER
       to_list = [myuser.email]
       send_mail(subject, message, from_email, to_list, fail_silently=True)
       print(2)


       #Email address confirmation email

       current_site = get_current_site(request)
       email_subject = "Confirm your email for Nepashraya login"
       message2 = render_to_string('email_confirmation.html', {

           'name': myuser.first_name,
           'domain': current_site.domain,
           'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
           'token': generate_token.make_token(myuser),
       })
       print(3)
       email = EmailMessage(
                            email_subject,
                            message2,
                            settings.EMAIL_HOST_USER,
                            [myuser.email],
                            )
       email.fail_silently = True
       email.send()
       print(4)


       return render(request, 'auth/landingpage.html')
       print(5)
    return render(request, 'auth/signup.html')

def activate(request,uidb64,token):
    print(1)
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk = uid)
    

    except (TypeError,ValueError,OverflowError,User.DoesNotExist):
        myuser = None
    print(2)

    if myuser is not None and generate_token.check_token(myuser, token):
        myuser.is_active = True
        myuser.save()
        print(3)
        login(request, myuser)
        print(4)
        messages.success(request, "Your Account has been activated!!")
        print(5)
        return render(request, 'auth/landingpage.html')
    else:
        return render(request, 'auth/activation_failed.html')
    
def signin(request):
    print(1)
    if request.method == "POST":
       print(2)

       username = request.POST['username']
       pass1 = request.POST['pass1']

       user = authenticate(username=username, password=pass1)
       print(3)


       if user is not None:
          login(request, user)
          fname = user.first_name
          print(4)
          return redirect("upload")
       else:
          print(5)
          messages.error(request, "Bad credentials")
          print(6)

          return redirect('authregister')
    return render(request, "auth/landingpage.html")


def signout(request):
    logout(request)
    messages.success(request, "Logged Out successfully.")
    return redirect('index')

# def create_post(request):
#     return render(request, 'post_form.html') # yeha post_form ko html file banauna parney

