from django.db import models
from django.core.validators import EmailValidator
from django.utils import timezone
from django.contrib.auth.models import User
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
    post_date = models.DateTimeField(default=timezone.now, null=True, blank=True)

    class Meta:
        ordering = ['-post_date']
    

class Topic(models.Model):
    title = models.CharField(max_length=100)
    long_description = models.TextField()
    category = models.ManyToManyField("Category", related_name='topics')
    province = models.ForeignKey(province, on_delete=models.CASCADE, related_name='topics')
    post_date = models.DateTimeField(default=timezone.now)
    is_verified = models.BooleanField(default=False)
    author = models.CharField(max_length=100, default="Anonymous")
    likes = models.ManyToManyField(User, related_name='topic', blank=True)
    report = models.IntegerField(User, default=0)
    commentCount = models.IntegerField(default=0, null=True, blank=True)
    views = models.IntegerField(default=0)


    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-post_date']
    
    def total_likes(self):
        return self.likes.count()
    
class Report_Post(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    

    class Meta:
        unique_together = ('topic', 'user')

class T_Image(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='topic_images')

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='category_images')

    def __str__(self):
        return self.name

class Comment(models.Model):
   author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commenter")
   content = models.TextField()
   post = models.ForeignKey(Topic, on_delete=models.CASCADE, default=None, null=True, blank=True
   )
   postedOn = models.DateTimeField(auto_now=True, blank=True)


   class Meta:
       ordering = ["-postedOn"]


   def __str__(self):
       return f"{self.content}"