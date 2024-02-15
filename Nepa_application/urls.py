from django.urls import path
# from . import views
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('contact_us/', views.contact_us, name='contact'),
    path('register/', views.register, name='register'),
    path('discover/', views.discover, name='discover'),
    path('search/', views.search, name='search'),
    
    path('province/<str:province>/', views.provience_clicked, name='province'),
    path('category/<str:category>/', views.category_clicked, name='category'),

    path('create/', views.create, name = 'create'),
    path('createe/', views.create_topic, name='create_topic'),
    path('listofpost/', views.listofpost, name='listofpost'),

]