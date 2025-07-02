from django import forms
from .models import DiscussionPost

class DiscussionPostForm(forms.ModelForm):
    class Meta:
        model = DiscussionPost
        fields = ['title', 'content', 'image', 'location']  # include image + location
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }