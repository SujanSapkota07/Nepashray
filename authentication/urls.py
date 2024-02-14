from . import views
from django.urls import path

urlpatterns = [
    path('register/', views.landingpage, name="authregister"),
    path('signup/', views.signup, name="authsignup"),
    path('activate/<uidb64>/<token>/', views.activate, name = "activate"),
    path('signin/', views.signin, name = "authsignin"),
    path('signout/', views.signout, name = "signout"),



]