from django.db import models

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
    