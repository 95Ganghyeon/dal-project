from django import forms
from django.utils.translation import gettext_lazy as _

from .models import User_story_origin

class UserStroyForm(forms.ModelForm):
    class Meta:
        model = User_story_origin
        fields = ('title', 'content', 'image1', 'image2')
        widgets = {
            'content': forms.Textarea(attrs={'placeholder': '자유롭게 자신의 이야기를 나누어주세요'}),
        }
        labels = {
            'title': _('제목'),
            'content': _('내용'),
        }