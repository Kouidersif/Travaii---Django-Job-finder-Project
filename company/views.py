
from django.shortcuts import render,get_object_or_404, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse
from main.forms import JobForm
from .models import CompanyProfile, Photos_c
from main.models import User, Jobs, Applying
from subscriptions.models import Customer
from .forms import CompanySignUpForm, CompanyProfileForm, UpdateUserForm, Cancel_SubscForm, PhotoForm
from django.views.generic import CreateView, View, UpdateView, TemplateView, DeleteView
from applicants.mixins import CompanyAndLogin
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login
from .decorators import notLogged, only_non_authenticated
import stripe
from django.conf import settings
import datetime
from django.contrib.auth.decorators import login_required
from subscriptions.models import ProName
from django.contrib import messages
from .myfilter import ApplicantsFilter
from datetime import date
from subscriptions.decorators import check_sub
from applicants.models import ApplicantProfile
from applicants.views import Confirm_message
import random
from main.models import Get_industry, number_user_facebook
from main.forms import ContactForm

from django.core.paginator import Paginator
#Your password can’t be too similar to your other personal information.
#Your password must contain at least 8 characters.
#Your password can’t be a commonly used password.
#Your password can’t be entirely numeric.





def LandingPage(request):
    try:
        from_where = 'fbclid'
        if from_where in request.GET:
            count, created = number_user_facebook.objects.get_or_create()
            count.users_l += 1
            count.save()
    except:
        pass
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
    return render(request, 'company/my/landingpage.html', {'form':form})










@only_non_authenticated
def Signup_as_company(request):
    form = CompanySignUpForm()
    if request.method == 'POST':
        form = CompanySignUpForm(request.POST)
        if form.is_valid():
            company= form.save()
            company.is_company= True
            company.save()
            new_co= authenticate(
                username= form.cleaned_data['username'], 
                password= form.cleaned_data['password1']
            )
            login(request, new_co)
            Confirm_message(request, request.user, request.user.email)
            return redirect('company_setup')
        
    else:
        CompanySignUpForm()
    return render(request,'company/register.html', {'form':form} )


@notLogged
def Company_setup(request):
    form = CompanyProfileForm()
    if request.method == 'POST':
        form = CompanyProfileForm(request.POST, request.FILES)
        if form.is_valid():
            company = form.save(commit=False)
            company.owner= request.user   
            company.is_profile_completed = True       
            company.save()
            try:
                company_input = request.POST.get('industry')
                Get_industry.objects.create(
                    industry_name = company_input
                )
            except:
                pass
            return redirect('email_confirm')
            

    else:
        form = CompanyProfileForm()

    
    return render(request, 'company/my/companyinfo.html',{'form':form})


def Setup_Profile(request, pk):
    data = User.objects.get(id=pk)
    co_data= CompanyProfile.objects.filter(owner__id=pk)
    publisher= Jobs.objects.filter(publisher__id=pk)
    app= Applying.objects.filter(id=pk)
    photos= Photos_c.objects.filter(photo_publisher__id= pk, is_public=True)
    
    context={
    'data':data, 'co_data':co_data, 'publisher': publisher, 'app':app, 'photos':photos
    }
    return render(request, 'company/my/company_profile.html', context)





def Side_Bar(request):
    co_data= CompanyProfile.objects.filter(owner=request.user)
    if co_data:
        print('GOOD')
    else:
        print('false')
    context = {'co_data':co_data}
    return render(request, 'company/co_sidebar.html', context)


@notLogged
@check_sub
def U_Profile(request, pk):
    data = User.objects.get(id=pk)
    co_data= CompanyProfile.objects.filter(owner=request.user)
    publisher= Jobs.objects.filter(publisher__id=pk)
    app= Applying.objects.filter(id=pk)

    if request.user.is_authenticated and request.user == data:
        if request.method == 'POST':
            form1= UpdateUserForm(request.POST, request.FILES, instance=data)
            if form1.is_valid():
                form1.save()
                messages.success(request, 'Info Updated')
                return redirect(request.META['HTTP_REFERER'])
        else:
            form1= UpdateUserForm(instance=data)
    else:
        return redirect('error_page')
    
    

    context={
    'data':data, 'co_data':co_data, 'publisher': publisher, 'app':app,
    'form1':form1
    }
    return render(request, 'company/my/co_manager.html', context)



@notLogged
def account_categories(request):
    return render(request, 'company/account_options.html')



@notLogged
@check_sub
def manage_subscription(request):
    
    co_data= CompanyProfile.objects.filter(owner=request.user)
    try:
        stripe_customer = Customer.objects.get(user=request.user)
        customer_data= stripe.Customer.retrieve(stripe_customer.stripeid)
        stripe.api_key = settings.STRIPE_SECRET_KEY
        subscription = stripe.Subscription.retrieve(stripe_customer.stripe_subscription_id)
        product = stripe.Product.retrieve(subscription.plan.product)
        user_balance = abs(customer_data.balance)
        end_date = datetime.datetime.fromtimestamp(subscription.current_period_end)
        start_date= datetime.datetime.fromtimestamp(subscription.current_period_start)
        all_invoices = stripe.Invoice.list(limit=10,
        customer = stripe_customer.stripeid,
        )
            
        
        payment_method = stripe.Customer.list_payment_methods(
            customer=stripe_customer.stripeid,
            type="card",
            )
        intent = stripe.SetupIntent.create(
            customer=stripe_customer.stripeid,
            payment_method_types=["card"],
            )
        last4digits = payment_method['data']
        
            
        context={'customer_data':customer_data,'user_balance':user_balance,'last4digits':last4digits,
            'subscription':subscription, 'product':product, 'end_date':end_date,  'co_data':co_data,
            'start_date':start_date, 'stripe_customer':stripe_customer,'all_invoices':all_invoices
        , 'client_secret':intent.client_secret}
        return render(request, 'company/manage_sub.html', context)
    except Customer.DoesNotExist:
        co_data= CompanyProfile.objects.filter(owner=request.user)
        return render(request, 'company/manage_sub.html', {'co_data':co_data})
        context= {
                'co_data':co_data
            }
    return render(request, 'company/manage_sub.html', context)



def retry_payment(request):
    try:
        stripe_customer = Customer.objects.get(user=request.user)
        stripe.api_key = settings.STRIPE_SECRET_KEY
        subscription = stripe.Subscription.retrieve(stripe_customer.stripe_subscription_id)
        product = stripe.Product.retrieve(subscription.plan.product)
        invoice = stripe.Invoice.retrieve(subscription.latest_invoice)
        invoice.pay()
        messages.success(request, 'Thanks!Your subscription has been re-activated now!')
        return redirect(request.META['HTTP_REFERER'])
    except stripe.error.CardError as e:
        messages.warning(request, 'Your card was declined')
        return redirect(request.META['HTTP_REFERER'])









@notLogged
def Make_card_default(request, card_id):
    try:
        stripe_customer = Customer.objects.get(user=request.user)
        stripe.api_key = settings.STRIPE_SECRET_KEY
        subscription = stripe.Subscription.retrieve(stripe_customer.stripe_subscription_id)
        product = stripe.Product.retrieve(subscription.plan.product)
        stripe.Customer.modify(
                            stripe_customer.stripeid,
                            invoice_settings ={
                            'default_payment_method':card_id,
                            }
                            )
        messages.success(request, 'New card has been set to Default')
        return redirect(request.META['HTTP_REFERER'])
    except:
        return HttpResponse('Permission Error')






@notLogged
def Delete_PM(request, card_id):
    try:
        stripe.PaymentMethod.detach(
                card_id,
                )
        messages.success(request, 'Card has been removed')

        return redirect(request.META['HTTP_REFERER'])
    except:
        return HttpResponse('Permission Error')



@notLogged
def Cancel_sub_or_reactivate(request, subscription_id):
    try:
        subscriber = Customer.objects.filter(user= request.user)
        stripe_customer = Customer.objects.get(user=request.user)
        stripe.api_key = settings.STRIPE_SECRET_KEY
        subscription = stripe.Subscription.retrieve(stripe_customer.stripe_subscription_id)
        product = stripe.Product.retrieve(subscription.plan.product)
        if subscription.cancel_at_period_end == False and stripe_customer.cancel_at_period_end == False :
            stripe.Subscription.modify(
                    subscription_id,
                    cancel_at_period_end=True
                    )
            subscriber.update(
                cancel_at_period_end = True,
            )
            
            messages.info(request, 'Subscription Canceled, You will still be able to enjoy services untill the end of your subscription ')
            return redirect(request.META['HTTP_REFERER'])
        elif subscription.cancel_at_period_end == True and stripe_customer.cancel_at_period_end == True:
            stripe.Subscription.modify(
                    subscription_id,
                    cancel_at_period_end=False
                    )
            subscriber.update(
                cancel_at_period_end = False,
            )
            
            
            messages.success(request, 'Subscription Reactivated!, Nice to see you again')
            return redirect(request.META['HTTP_REFERER'])
        
    except:
        return HttpResponse('Permission Error')



@notLogged
@check_sub
def UpdateCompany(request, pk):
    edit_info= get_object_or_404(CompanyProfile, id=pk)
    co_data= CompanyProfile.objects.filter(owner=request.user)
    
    if edit_info.owner == request.user:
        if request.method == 'POST':
                form= CompanyProfileForm(request.POST, request.FILES, instance=edit_info)
                if form.is_valid():
                    form.save()
                    messages.success(request, 'Info Updated')
                    return redirect(request.META['HTTP_REFERER'])
                else:
                    messages.warning(request, form.errors)
        else:
            form= CompanyProfileForm(instance=edit_info)
    else:
        return redirect('error_page')

    context= {
        'co_data':co_data,'form':form
    }
    return render(request, 'company/my/update_company.html', context )

@notLogged
@check_sub
def PostPhotos(request):
    form = PhotoForm()
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            publisher = form.save()
            publisher.photo_publisher= request.user
            publisher.is_public = True
            publisher.save()
            messages.success(request, 'Photo published')
            return redirect(request.META['HTTP_REFERER'])
            
        else:
            print(form.errors)
    else:
        PhotoForm()
    return render(request, 'company/my/post_photo.html', {'form':form})


@notLogged
def Edit_photo_privacy(request, pk):
    edit_info= get_object_or_404(Photos_c, id=pk)
    
    form = PhotoForm()
    if request.user.is_authenticated and edit_info.photo_publisher == request.user: 
        if request.method == 'POST':
            form = PhotoForm(request.POST, request.FILES, instance=edit_info)
            if form.is_valid():
                publisher = form.save()
                publisher.save()
                messages.success(request, 'Photo Edited')
                return redirect(request.META['HTTP_REFERER'])
        else:
            form = PhotoForm(instance=edit_info)
    else:
        return redirect('error_page')
    context= {
        'form':form, 'edit_info':edit_info
    }
    return render(request, 'company/my/edit_photo.html', context)

def View_all(request, pk):
    own = User.objects.get(id=pk)
    photos= Photos_c.objects.filter(photo_publisher=own)
    
    context= {
        'photos':photos
    }
    return render(request, 'company/my/view_photos.html', context)



@notLogged
def DeletePhotos(request, pk):
    photo_delete = get_object_or_404(Photos_c, id = pk)
    if request.method =="POST":
        photo_delete.delete()
        messages.success(request, 'Photo deleted')
        return redirect(request.META['HTTP_REFERER'])
    return render(request, 'company/my/delete_photo.html', {'photo_delete':photo_delete})



@notLogged
def view_application(request):
    if request.user.is_authenticated and request.user.is_company:
        to_filter= ApplicantsFilter(request.GET, queryset=Applying.objects.filter(job__publisher=request.user))
        applications = to_filter.qs
        paginator = Paginator(applications, 7)
        page_number = request.GET.get('page', 1)
        page_objects = paginator.page(page_number)
    else:
        return redirect('error_page')
    return render(request, 'company/view_application.html', {'applications':applications, 'to_filter':to_filter,'paginator':paginator,  'page_number':page_number, 'page_objects':page_objects, })




@notLogged
@check_sub
def Apps_jobs(request):
    if request.user.is_authenticated and request.user.is_company:
        myjobs=Jobs.objects.filter(publisher=request.user).order_by('-creation_date')
        paginator = Paginator(myjobs, 10)
        page_number = request.GET.get('page', 1)
        page_objects = paginator.page(page_number)
        context= {'myjobs':myjobs,'page_objects': page_objects, 'paginator': paginator}
    else:
        return redirect('error_page')
    return render(request, 'company/my/manage_jobs.html', context)




### Save Applicant 


@login_required
def SaveApplicant(request, id):
    to_save= get_object_or_404(ApplicantProfile, id=id)
    if to_save.save_applicant.filter(id=request.user.id).exists():
        to_save.save_applicant.remove(request.user)
        messages.success(request, "Applicant's profile removed")
    else:
        to_save.save_applicant.add(request.user)
        messages.success(request, 'Applicant Saved')
    return redirect(request.META['HTTP_REFERER'])


@login_required
def Saved_Profiles(request):
    applicants_list= ApplicantProfile.objects.filter(save_applicant=request.user)
    return render(request, 'company/my/saved_list.html', {'applicants_list':applicants_list})