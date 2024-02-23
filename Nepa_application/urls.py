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

    path('upload/', views.upload, name = 'upload'),
    path('createe/', views.create_topic, name='create_topic'),
    path('listofpost/', views.listofpost, name='listofpost'),

     # URL pattern for verifying a post
    path('verify_post/<int:topic_id>/', views.verify_post, name='verify_post'),
    
    # URL pattern for blocking a post
    path('block_post/<int:topic_id>/', views.block_post, name='block_post'),

    # url for managing usser
    path('manageuser/', views.manage_user, name='manage_user'),
    # url to delete a user
    path('delete/<int:user_id>/', views.delete_user, name='delete'),

    #detailed view of a document
    path('detailed_view/<int:topic_id>/', views.detailed_view, name= 'detailed_view'),

    #report the post
    path('report/<int:topic_id>/', views.report, name='report'),

    #like the post
    path('like/<int:post_id>/', views.like_post, name='like_post'),
    path('unlike/<int:post_id>/', views.unlike_post, name='unlike_post'),

    path("addcomment<id>/",views.add_comment, name="add-comment"),

     ]