from django.shortcuts import render, redirect, get_object_or_404
from .models import Article, Tags
from .forms import BlogNewsLetterForm, PostBlogForm
from django.views.generic import FormView, CreateView






class BlogHome(FormView):
    form_class = BlogNewsLetterForm
    template_name = 'main.html'
    def form_valid(self, form):
        form.save()
        return redirect(self.request.META['HTTP_REFERER'])
    def get(self, request):
        blogs = Article.objects.all()
        tags = Tags.objects.all()
        context= {
        'blogs':blogs,
        'tags': tags,
        "form":self.form_class
        }
        return render(request, 'main.html', context)





class CreateBlog(CreateView):
    form_class = PostBlogForm
    template_name = 'blog_create.html'
    def form_valid(self, form):
        job = form.save(commit=False)
        job.author_name = self.request.user
        job.save()
        return redirect('blog-home')


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