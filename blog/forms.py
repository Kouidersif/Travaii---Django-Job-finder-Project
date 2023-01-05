from django.forms import ModelForm
from .models import *

class BlogNewsLetterForm(ModelForm):
    class Meta:
        model = BlogNewsLetter
        fields = ['email']

    def __init__(self, *args, **kwargs):
        super(BlogNewsLetterForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter Email'


class PostBlogForm(ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content', 'blog_media','category', 'thumbnail', 'tags', 'slug' ]

    def __init__(self, *args, **kwargs):
        super(PostBlogForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs['class'] = 'form-control'
        self.fields['content'].widget.attrs['class'] = 'form-control'
        self.fields['blog_media'].widget.attrs['class'] = 'form-control'
        self.fields['category'].widget.attrs['class'] = 'form-select'
        self.fields['thumbnail'].widget.attrs['class'] = 'form-control'
        self.fields['tags'].widget.attrs['class'] = 'js-select form-select'
        self.fields['slug'].widget.attrs['class'] = 'form-control'

        