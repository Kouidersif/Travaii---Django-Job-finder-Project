import stripe
from stripe import Subscription
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.conf import settings
from django.http.response import JsonResponse # new
from django.views.decorators.csrf import csrf_exempt # new
from django.http import HttpResponse
from django.views import generic
from django.http import HttpResponseRedirect
from subscriptions.models import Customer
from datetime import timedelta
from .forms import *
from applicants.mixins import CompanyAndLogin
from django.contrib import messages
from .models import *
from company.models import CompanyProfile
from applicants.models import *
from django.contrib.auth.views import PasswordChangeView
from applicants.forms import *
from django.contrib.auth.forms import PasswordChangeForm
from .filters import *
from django.contrib.auth.decorators import login_required
from subscriptions.decorators import check_sub
from django.core.mail import EmailMessage
from django.template.loader import render_to_string, get_template
from django.core.mail import EmailMultiAlternatives
from django.template import Context
from django.core.paginator import Paginator
import random




def PrivacyPolicy(request):
    return render(request, 'privacy_policy.html')


#Your password can’t be too similar to your other personal information.
#Your password must contain at least 8 characters.
#Your password can’t be a commonly used password.
#Your password can’t be entirely numeric.


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
        


    


@login_required 
@check_sub
def CreateJob(request):
    
    user = User.objects.get(id=request.user.id)
    try:
        if request.user.customer.membership:
            c = Customer.objects.filter(user= request.user)
            stripe_customer = Customer.objects.get(user=request.user)
            #print(user.work.count())
            
            stripe.api_key = settings.STRIPE_SECRET_KEY
            subscription = stripe.Subscription.retrieve(stripe_customer.stripe_subscription_id)
            d = datetime.datetime.fromtimestamp(subscription.current_period_end)
            #print(d)
            product = stripe.Product.retrieve(subscription.plan.product)
            
            #print(product.name)
            ##Small business PLAN 
            if request.user.customer.selected_membership == 'Small business':
                
                if subscription.current_period_end != datetime.date.today() and subscription.status == 'active':
                    # need to add max can be published for each plan
                    if user.work.count() >= 2:
                        return render(request, 'upgrade_message.html' )
                    else:
                        form = JobForm()
                        if request.method == 'POST':
                            form = JobForm(request.POST)
                            if form.is_valid():
                                job = form.save(commit=False)
                                job.publisher= request.user
                                job.save()
                                job.is_published=True
                                job.save()
                                return redirect('alljobs')
                            else:
                                messages.warning(request, form.errors)
                        else:
                            form = JobForm()
                        info={
                            'form': form
                            }
                    return render(request, 'main/crud/create_job.html',info )
                else:
                    return render(request, 'upgrade_message.html' )
            #### Mid-market enterprises PLAN
            elif request.user.customer.selected_membership == 'Mid-market enterprises':
                
                if subscription.current_period_end != datetime.date.today() and subscription.status == 'active':
                    # need to add max can be published for each plan
                    if user.work.count() >= 5:
                        return render(request, 'upgrade_message.html' )
                    else:
                        form = JobForm()
                        if request.method == 'POST':
                            form = JobForm(request.POST)
                            if form.is_valid():
                                job = form.save(commit=False)
                                job.publisher= request.user
                                job.save()
                                job.is_published=True
                                job.save()
                                return redirect('alljobs')
                            else:
                                messages.warning(request, form.errors)
                        else:
                            form = JobForm()
                        info={
                            'form': form
                            }
                    return render(request, 'main/crud/create_job.html',info )
                else:
                    return render(request, 'upgrade_message.html' )
                


            #### LARG   enterprise PLAN 
            elif request.user.customer.selected_membership == 'Large enterprise':
                
                if subscription.current_period_end != datetime.date.today() and subscription.status == 'active':
                    # need to add max can be published for each plan
                    if user.work.count() >= 5:
                        return render(request, 'upgrade_message.html' )
                    else:
                        form = JobForm()
                        if request.method == 'POST':
                            form = JobForm(request.POST)
                            if form.is_valid():
                                job = form.save(commit=False)
                                job.publisher= request.user
                                job.save()
                                job.is_published=True
                                job.save()
                                return redirect('alljobs')
                            else:
                                messages.warning(request, form.errors)
                        else:
                            form = JobForm()
                        info={
                            'form': form
                            }
                    return render(request, 'main/crud/create_job.html',info )
            else:
                return render(request, 'upgrade_message.html' )

    except Customer.DoesNotExist:
        if user.work.count() >= 1:
            return render(request, 'upgrade_message.html' )
        else:
            form = JobForm()
            if request.method == 'POST':
                form = JobForm(request.POST)
                if form.is_valid():
                    job = form.save(commit=False)
                    job.publisher= request.user
                    job.save()
                    job.is_published=True
                    job.save()
                    return redirect('alljobs')
                else:
                    messages.warning(request, form.errors)
            else:
                form = JobForm()
            info={
                'form': form
                }
            return render(request, 'main/crud/create_job.html', info )
        

    
### need to work on form.errors Create job



@check_sub
def HomePage(request):

    jobs=Jobs.objects.all()
    
    companies=CompanyProfile.objects.all()
    candidates=ApplicantProfile.objects.filter(is_public=True)
    categ= Category.objects.all()
    s = Wilaya.objects.all()
    context={'jobs':jobs, 'categ':categ, 'companies':companies, 'candidates':candidates}
    return render(request, 'main/index.html', context)


def Search_for(request):
    if request.method == 'POST':
        searched= request.POST['searched']
        jobs=Jobs.objects.filter(position__contains=searched)
        context={'searched':searched, 'jobs':jobs}

        return render(request, 'search_for.html', context)
    else:
        return render(request, 'search_for.html')
    





def Test(request):
    #message = EmailMessage(mail_subject, html_message,to=['islamkouider61@gmail.com'])
    #message.content_subtype = 'html' # this is required because there is no plain text email version
    #message.send()
    
    return render(request, 'test.html')
    



def ConfirmEmailPage(request):
    return render(request, 'email_confirm.html')



def Contact(request):
    form = ContactForm()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you for reaching us, we will be back to you as soon as possible')
            return redirect(request.META['HTTP_REFERER'])
        else:
            messages.success(request, form.errors)
    else:
        ContactForm()
    context= {
        'form':form
    }
    return render(request, 'contact.html', context)



@check_sub
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






@login_required
def DeleteUser(request, pk):
    user = User.objects.get(id=pk)
    try:
        if request.method == 'POST':
            user_reason= request.POST.get('user_field')
            text_field = request.POST.get('textfield')
            Delete_account_Feedback.objects.create(
                the_reason = user_reason,
                reason_txt= text_field,
                email_user = request.user.email,
            )
            user.delete()
            mail_subject = 'Travaii Team: Account has been deleted'
            templ = render_to_string('account_deleted.html', {
                'name':request.user.full_name,
            })
            success_email = EmailMessage(
                        mail_subject, templ, 
                        to=[request.user.email],
                    )
            success_email.send()
            return redirect('log_in')
    except:
        pass
    return render(request, 'users/delete_account.html')






class UpdateJob(CompanyAndLogin, generic.UpdateView):
    
    template_name= 'main/crud/update_job.html'
    queryset= Jobs.objects.all()
    form_class = JobForm
    
    def get_success_url(self):
        messages.success(self.request, 'Your changes have been saved.')
        return reverse('manage_jobs')

@check_sub
def DetailJob(request, pk):
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
def SaveJob(request, id):
    to_save= get_object_or_404(Jobs, id=id)
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
    return render(request, 'error_page/Error.html')