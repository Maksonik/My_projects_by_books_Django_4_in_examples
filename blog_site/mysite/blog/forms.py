from django import forms
from .models import Comment


class SearchForm(forms.Form):
    query= forms.CharField()


class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField(max_length=50)
    to = forms.EmailField(max_length=50)
    comment = forms.CharField(max_length=200,
                              required=False,
                              widget=forms.Textarea)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'body']
