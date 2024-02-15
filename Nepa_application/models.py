from django.db import models
from django.core.validators import EmailValidator

# Create your models here.

# creating a model for 7 provience that contains name, capital description and image using cloudinary


class province(models.Model):
    name = models.CharField(max_length=100)
    capital = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='Provience_Image/')

    def __str__(self):
        return self.name

class image(models.Model):
    image = models.ImageField(upload_to='all_image/')
    provience = models.ForeignKey(province, on_delete=models.CASCADE, related_name = 'images')
  
    

class Contact_us(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(validators=[EmailValidator(message='Enter a valid email address.')])
    phone = models.CharField(max_length=10)  # Adjust length as needed
    text_message = models.TextField()


class Topic(models.Model):
    title = models.CharField(max_length=100)
    long_description = models.TextField()
    category = models.ManyToManyField('Category', related_name='topics')
    province = models.ForeignKey(province, on_delete=models.CASCADE, related_name='topics')

    def __str__(self):
        return self.title

class T_Image(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='topic_images')

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='category_images')
    def __str__(self):
        return self.name