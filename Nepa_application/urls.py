from django.urls import path
# from . import views
from . import views
from django.contrib.auth import views as auth_views

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

    # URL pattern for viewing  a post
    path('view_post/<int:topic_id>/', views.view_post, name='view_post'),
    
    # to view all the contact us contents
    path('view_contact/', views.admin_contacts, name='admin_contacts'),
    # url for managing usser
    path('manageuser/', views.manage_user, name='manage_user'),
    # url to delete a user
    path('delete/<int:user_id>/', views.delete_user, name='delete'),

    #detailed view of a document
    path('detailed_view/<int:topic_id>/', views.detailed_view, name= 'detailed_view'),

    #report the post
    path('report/<int:topic_id>/', views.report, name='report'),

    # #like the post
    # path('like/<int:post_id>/', views.like_post, name='like_post'),
    # path('unlike/<int:post_id>/', views.unlike_post, name='unlike_post'),

    path("addcomment<id>/",views.add_comment, name="add-comment"),

    # for forget password
    # path('forgot-password/', views.forgot_password, name='forgot_password'),
    # path('reset-password/confirm/<uidb64>/<token>/', views.reset_password_confirm, name='password_reset_confirm'),
    # path('reset-password/complete/', views.reset_password_complete, name='password_reset_complete'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='password_reset.html'), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name = 'reset_password_confirm.html'), name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='reset_password_complete.html'), name='password_reset_complete'),


    # path('password_reset/', auth_views.PasswordResetView.as_view(template_name='password_reset_form.html'), name='password_reset'),
    # path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    # path('password_reset_confirm/uidb64/token/',auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    # path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),

]