from django import forms
from . import models
# from .models import provience

# class ProvienceForm(forms.ModelForm):
#     class Meta:
#         model = provience
#         fields = ['name', 'capital', 'description', 'image']

class contact(forms.ModelForm):
    class Meta:
        model  = models.Contact_us
        fields = ['name', 'email', 'phone', 'text_message']
    


class TopicForm(forms.ModelForm):
    # images = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
    class Meta:
        model = models.Topic
        fields = ['title', 'long_description', 'category', 'province']

    