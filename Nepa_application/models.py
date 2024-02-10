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
  
    

class Contact_us(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(validators=[EmailValidator(message='Enter a valid email address.')])
    phone = models.CharField(max_length=10)  # Adjust length as needed
    text_message = models.TextField()


class Topic(models.Model):
    title = models.CharField(max_length=100)
    short_description = models.CharField(max_length=200)
    long_description = models.TextField()

class T_Image(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='topic_images')
