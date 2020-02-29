from django import forms

from .models import User_story_origin

class User_story_origin_form(forms.ModelForm):
    class Meta:
        model = User_story_origin
        fields = ("title", "content", "image1", "image2")

