from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model  = Comment
        fields = ['name', 'email', 'body']
        widgets = {
            'name':  forms.TextInput(attrs={
                'placeholder': 'Your name',
                'class': 'form-input',
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'your@email.com (never published)',
                'class': 'form-input',
            }),
            'body':  forms.Textarea(attrs={
                'placeholder': 'Share your thoughts...',
                'class': 'form-textarea',
                'rows': 4,
            }),
        }
        labels = {
            'name':  'Name',
            'email': 'Email',
            'body':  'Comment',
        }
