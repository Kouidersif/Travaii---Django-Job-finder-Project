from django.db import models
from django.utils.text import slugify
from ckeditor.fields import RichTextField
from django.utils import timezone
from main.models import User

now = timezone.now





class Article(models.Model):
    author_name= models.ForeignKey(User, models.SET_NULL, null=True)
    title = models.CharField(max_length=255, null=True)
    content = RichTextField(config_name='awesome_ckeditor')
    category = models.ForeignKey('ArticleCategory', related_name='articlecategory',on_delete=models.SET_NULL, null=True)
    blog_media= models.ImageField(blank=True, null=True, upload_to='images/blog/') #1920x1080 recommeded
    thumbnail= models.ImageField(blank=True, null=True, upload_to='images/blog/thumbnail/')
    tags = models.ManyToManyField('Tags',blank=True )
    slug = models.SlugField(unique=True, blank=True)
    updated_on = models.DateTimeField(auto_now_add=now)
    Created_on = models.DateTimeField(auto_now_add=now)
    public = models.BooleanField(default=True, null=True, blank=True)
    def __str__(self):
        return self.title
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.id and not self.slug:
            self.slug = slugify(f'{self.id}-{self.category}-{self.title}')
        super().save(*args, **kwargs)


class Tags(models.Model):
    tag_name= models.CharField(max_length=100, null=True, blank=True)
    def __str__(self):
        return self.tag_name

class ArticleCategory(models.Model):
    title = models.CharField(max_length=300)
    def __str__(self):
        return self.title

class BlogNewsLetter(models.Model):
    email = models.EmailField()
    receive_blogs = models.BooleanField(default=True)

class Announcements(models.Model):
    title = models.CharField(max_length=250, null=True, blank=True)
    image = models.ImageField(upload_to='images/blog/announcement', null=True)
    body= RichTextField(config_name='awesome_ckeditor')
