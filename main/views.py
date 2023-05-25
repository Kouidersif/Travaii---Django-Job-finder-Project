from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.conf import settings
from django.http import HttpResponse
from django.views import generic
from .forms import *
from applicants.mixins import CompanyAndLogin
from django.contrib import messages
from .models import *
from company.models import CompanyProfile
from applicants.models import *
from django.contrib.auth.views import PasswordChangeView
from applicants.forms import *
from .filters import *
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.core.paginator import Paginator
from applicants.forms import NewsLetterForm
from .tasks import Notify_user_account_deleted
from django.contrib.auth.mixins import LoginRequiredMixin











def PrivacyPolicy(request):
    return render(request, 'privacy_policy.html')





class PwdChange(PasswordChangeView):
    form_class= PwdChangingForm
    success_url= reverse_lazy('changed')





def Successpwd(request):
    return render(request, 'registration/success_pwd_change.html')





class UpdateStatus(CompanyAndLogin,generic.UpdateView):
    model= Applying
    
    template_name= 'company/my/edit_apps.html'
    
    form_class = EditApplyForm
    
    def get_success_url(self):
        return reverse('view_application')
        


    





class CreateJobView(CompanyAndLogin, generic.CreateView):
    form_class = JobForm
    template_name = 'main/crud/create_job.html'
    
    def form_valid(self, form):
        
        job = form.save(commit=False)
        job.publisher = self.request.user
        job.is_published = True
        job.save()
        return redirect('alljobs')








class HomePage(generic.FormView):
    form_class = NewsLetterForm
    template_name = 'main/index.html'
    def get(self, request):
        jobs=Jobs.objects.filter(is_published=True)
        companies=CompanyProfile.objects.all()
        candidates=ApplicantProfile.objects.filter(is_public=True)
        categ= Category.objects.all()
        s = Wilaya.objects.all()
        form = NewsLetterForm()
        f = SnippetFilter(request.GET, queryset=Jobs.objects.filter(is_published=True))
        all_jobs = f.qs
        categories = category= Category.objects.all()
        context={'jobs':jobs, 'companies':companies, 'f':f,'all_jobs':all_jobs,'categories':categories, 'candidates':candidates, 'form':form}
        return render(request, self.template_name, context)  
    def form_valid(self, form):
        form.save()
        return redirect('sign_up')
    



def Search_for(request):
    if request.method == 'POST':
        searched= request.POST['searched']
        jobs=Jobs.objects.filter(position__contains=searched)
        context={'searched':searched, 'jobs':jobs}

        return render(request, 'search_for.html', context)
    else:
        return render(request, 'search_for.html')
    





# def Test(request):
#     mail_subject = 'hello'
#     html_message= 'hello testing'
#     from_email='support@travaii.com'
#     message = EmailMessage(mail_subject, html_message,from_email, to=['kouidersif04@gmail.com'])
#     message.content_subtype = 'html' # this is required because there is no plain text email version
#     message.send()
#     return HttpResponse('dibe')
#     #test


def ConfirmEmailPage(request):
    return render(request, 'email_confirm.html')





class Contact(generic.FormView):
    form_class = ContactForm
    template_name = 'contact.html'

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Thank you for reaching us, we will be back to you as soon as possible')
        return redirect(self.request.META['HTTP_REFERER'])
    
    def form_invalid(self, form):
        messages.success(self.request, form.errors)







def DisplayJobs(request):
    jobs= Jobs.objects.filter(is_published=True).order_by('-creation_date')
    f = SnippetFilter(request.GET, queryset=Jobs.objects.filter(is_published=True))
    filtered = f.qs
    paginator = Paginator(filtered, 10)
    page_number = request.GET.get('page', 1)
    page_objects = paginator.page(page_number)
    total_jobs= Jobs.objects.filter(is_published=True).count()
    category= Category.objects.all()
    j_type= Job_type.objects.all()
    w_from= Work_from.objects.all()
    context={'jobs':jobs,'total_jobs':total_jobs, 'category':category,'j_type':j_type, 'w_from':w_from, 'f':f
    ,'page_objects': page_objects, 'paginator': paginator}
    return render(request, 'main/display/display_jobs.html', context)







class DeleteUser(LoginRequiredMixin,generic.View):
    def get(self, request, pk):
        return render(request, 'users/delete_account.html')
    def post(self, request, pk):
        user = User.objects.get(id = pk)
        user_reason= request.POST.get('user_field')
        text_field = request.POST.get('textfield')
        Delete_account_Feedback.objects.create(
            the_reason = user_reason,
            reason_txt= text_field,
            email_user = request.user.email,
        )
        Notify_user_account_deleted.delay(
                pk
        )
        user.delete()
        return redirect("log_in")








class UpdateJob(CompanyAndLogin, generic.UpdateView):
    
    template_name= 'main/crud/update_job.html'
    queryset= Jobs.objects.all()
    form_class = JobForm
    
    def get_success_url(self):
        messages.success(self.request, 'Your changes have been saved.')
        return reverse('manage_jobs')
    



class DetailJob(generic.View):
    def get(self, request, pk):
        job = Jobs.objects.filter(id=pk)
        job2= get_object_or_404(Jobs, id=pk)  
        
        
        added= bool
        
        if job2.save_job.filter(id=request.user.id).exists():
            added=True
        #print(job2)
        applying= Applying.objects.filter(sender_id=request.user.id, job_id=job2.pk)
        context={
            'job':job, 'applying':applying, 'added':added
        }
        return render(request, 'main/crud/job_detail.html' , context)





class DeleteJob(CompanyAndLogin, generic.DeleteView):
    template_name= 'main/crud/delete_job.html'
    queryset= Jobs.objects.all()
    def get_success_url(self):
        return reverse('manage_jobs')





def CategoryView(request):
    view_cat= Category.objects.all().order_by('name')
    context= {'view_cat':view_cat}
    return render(request, 'main/category.html' ,context)




def Category_list(request, pk):
    cat_list= Jobs.objects.filter(job_category_id=pk)
    context= {'cat_list':cat_list}
    return render(request, 'main/display/display_cat.html', context)



@login_required
def SaveJob(request, pk):
    to_save= get_object_or_404(Jobs, id=pk)
    if to_save.save_job.filter(id=request.user.id).exists():
        to_save.save_job.remove(request.user)
        
    else:
        to_save.save_job.add(request.user)
        
    return redirect(request.META['HTTP_REFERER'])


@login_required
def ApplyList(request):
    myApply_list= Jobs.objects.filter(save_job=request.user).order_by('-creation_date')
    return render(request, 'main/saved_jobs.html', {'myApply_list':myApply_list})




def no_permission(request):
    return render(request, 'error_page/error.html')