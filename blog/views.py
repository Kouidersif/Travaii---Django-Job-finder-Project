from django.shortcuts import render, redirect, get_object_or_404
from .models import Article, Tags
from .forms import BlogNewsLetterForm, PostBlogForm
from django.views.generic import *
# Create your views here.


def BlogHome(request):
    blogs = Article.objects.all()
    tags = Tags.objects.all()
    if request.method == 'POST':
        form = BlogNewsLetterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(request.META['HTTP_REFERER'])
    else:
        form = BlogNewsLetterForm()
    context= {
        'blogs':blogs,
        'form':form,
        'tags': tags

    }
    return render(request, 'main.html', context)



def CreateBlog(request):
    form = PostBlogForm()
    if request.method == 'POST':
        form = PostBlogForm(request.POST, request.FILES)
        if form.is_valid():
            job = form.save(commit=False)
            job.author_name = request.user
            job.save()
            return redirect('blog-home')
    else:
        form = PostBlogForm()
    return render(request, 'blog_create.html', {'form':form})


def BlogDetails(request, pk, slug):
    blogs= get_object_or_404(Article, id=pk, slug=slug)
    
    related_blogs = Article.objects.filter(category = blogs.category).exclude(pk=pk)
    if request.method == 'POST':
        form = BlogNewsLetterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(request.META['HTTP_REFERER'])
    else:
        form = BlogNewsLetterForm()
    context = {'blogs':blogs, 'form':form, 'related_blogs':related_blogs}
        
    
    return render(request, 'blog.html', context)