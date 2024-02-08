from django.urls import path
# from . import views
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('contact_us/', views.contact_us, name='contact'),
    path('register/', views.register, name='register'),
    path('discover/', views.discover, name='discover'),
    path('search/', views.search, name='search'),
    path('province/', views.provience_clicked, name='province'),

]