from django.db import models
from django.core.validators import EmailValidator

# Create your models here.

# creating a model for 7 provience that contains name, capital description and image using cloudinary


class provience(models.Model):
    name = models.CharField(max_length=100)
    capital = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='Provience_Image/')

class image(models.Model):
    image = models.ImageField(upload_to='all_image/')
    provience = models.ForeignKey(provience, on_delete=models.CASCADE, related_name = 'images')
    

# this model is for the provience, when the provience is selected, this page open, and for the content of this page, model is made 
    
# class Landing_Provience(models.Model):
#     name = models.CharField(max_length=100)
#     major_description = models.TextField()
#     minor_description = models.TextField()
#     proviencenumber = models.CharField(max_length=10)
    

class Contact_us(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(validators=[EmailValidator(message='Enter a valid email address.')])
    phone = models.CharField(max_length=10)  # Adjust length as needed
    text_message = models.TextField()


# this is the model for creating posts
class Post(models.Model):
    image = models.ImageField(upload_to='posts/')
    post_name = models.CharField(max_length=100)
    postedby = models.CharField(max_length=100)
    description = models.TextField()
    likes = models.IntegerField(default=0)
    seen = models.IntegerField(default=0)