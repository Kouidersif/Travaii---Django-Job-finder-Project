

from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse
from .forms import *
from django.views.generic import CreateView, View, ListView, UpdateView, FormView, DeleteView
from main.models import *
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.views import generic
from main.forms import *
from .filtering import *
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from subscriptions.models import Customer
from django.conf import settings
import stripe
from .decorators import notApplicant
from .email_token import TokenGenerator
from .email_token import account_activation_token
from company.decorators import notLogged
from django.core.mail import EmailMessage
from django.template.loader import render_to_string, get_template
from django.contrib.sites.shortcuts import get_current_site  
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode  
from django.contrib.auth import get_user_model
from django.template import Context
from company.decorators import only_non_authenticated
import datetime



def activate(request, uidb64, token):
    user = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk= uid)
    except:
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_email_confirmed = True
        user.save()
        return redirect('email_confirm')
    else:
        messages.warning(request, f'Invalid Confirmation Link')
        return redirect('home')




@login_required
def CompanyResponse(request, pk):
    job = Applying.objects.get(id=pk)
    return render(request, 'users/view/respo.html', {'job':job})




def Confirm_message(request, user, to_email):
    try:
        mail_subject = 'Please activate your Account'
        from_email='support@travaii.com'
        templ = render_to_string('users/welcome_email.html', {
            'name':request.user.full_name,
            'domain':get_current_site(request).domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
            'protocol': 'https' if request.is_secure() else 'http',
        })
        ## sending html styled mail
        success_email = EmailMessage(
                    mail_subject, templ, from_email,
                    to=[to_email],
                )
        success_email.content_subtype = 'html'
        success_email.send()
    except:
        messages.warning(request, f'Email confirmation failed, please check if your email is correct {to_email}')


@only_non_authenticated
def Signup_as_applicant(request):
    #counting number of visits from facebook
    try:
        from_where = 'fbclid'
        if from_where in request.GET:
            count, created = number_user_facebook.objects.get_or_create()
            count.users_l += 1
            count.save()
    except:
        pass
    form= ApplicantSignUpForm()
    if request.method == 'POST':
        form = ApplicantSignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            user.is_applicant=True
            user.save()
            new_user= authenticate(
                username= form.cleaned_data['username'],
                password= form.cleaned_data['password1']
            )
            login(request, new_user)
            Confirm_message(request, user, request.user.email)
            return redirect('profile_setup')
        
        
    else:
        form =ApplicantSignUpForm()
    return render(request, 'users/registration/signup.html', {'form':form})
    



@login_required
def Profile(request, username):
    user= User.objects.get(username=username)
    applicants= ApplicantProfile.objects.filter(owner=user)
    myskills= Skills.objects.filter(owner=user)
    experience=Experience.objects.filter(owner=user)
    study= Education.objects.filter(student=user)
    return render(request, 'users/profile_page.html', {'user':user, 'applicants':applicants, 'study':study, 'myskills':myskills, 'experience':experience})



@login_required
@notApplicant
def Studies(request):
    form = EducationForm()
    if request.method== 'POST':
        form = EducationForm(request.POST)
        form2= SkillsForm(request.POST)
        if form.is_valid() and form2.is_valid():
            education = form.save(commit=False)
            education.student= request.user
            education.save()
            skill = form2.save(commit=False)
            skill.owner= request.user
            skill.save()
            return redirect('alljobs')
        else:
            print(form.errors, form2.errors)
            
            
            
    else:
        form = EducationForm()
        form2= SkillsForm()

    return render(request, 'users/info/education.html', {'form':form, 'form2':form2})



@login_required
@notApplicant
def Account_settings(request):
    return render(request, 'users/account_categories.html')



@login_required
@notApplicant
def ShowSkills(request):
    skills = Skills.objects.filter(owner=request.user)
    if request.method== 'POST':
        form = SkillsForm(request.POST)
        
        if form.is_valid():
            education = form.save(commit=False)
            education.owner= request.user
            education.save()
            return redirect(request.META['HTTP_REFERER'])
    else:
        form = SkillsForm()
    

    return render(request, 'users/info/skills/show_skills.html', {'skills':skills, 'form':form})







class DeleteSkill(generic.DeleteView):
    template_name= 'users/info/skills/delete_skill.html'
    queryset= Skills.objects.all()
    def get_success_url(self):
        return reverse('skills')






@login_required
@notLogged
def candidates(request):
    candidates=ApplicantProfile.objects.filter(is_public='Anyone').order_by('-applicant_cv')
    candid = CandidateFilter(request.GET, queryset=candidates)
    filtered = candid.qs
    paginator = Paginator(filtered, 10)
    page_number = request.GET.get('page', 1)
    page_objects = paginator.page(page_number)
    context={'candidates':candidates, 'candid':candid, 'paginator':paginator,'page_number':page_number,'page_objects':page_objects}
    return render(request, 'users/candidates.html', context)
    






def Applicant_cv(request):
    my_cv= ApplicantProfile.objects.filter(owner=request.user)
    return render(request, 'users/crud_users/cv_info.html', {'my_cv':my_cv})


















@login_required
def Applicant_Setup(request):
    form = ApplicantProfileForm()
    if request.user.is_authenticated and request.user.is_applicant:
        if request.method == 'POST':
            form = ApplicantProfileForm(request.POST, request.FILES)
            if form.is_valid():
                applicant = form.save(commit=False)
                applicant.owner= request.user
                applicant.save()
                applicant.submited = True
                applicant.save()
                return redirect('email_confirm')
            else:
                messages.warning(request, form.errors)
                
        else:
            form = ApplicantProfileForm()
    else:
        return redirect('error_page')
    info = {
        'form': form
    }
    return render(request, 'users/applicant_set_up.html' ,info )


@login_required
@notApplicant
def ShowProfile(request, pk):
    data = User.objects.get(id=pk)
    
    try:
        applicants=ApplicantProfile.objects.get(owner=pk)
        if request.user.is_authenticated and request.user == data:
            if request.method =='POST':
                form = ApplicantProfileForm(request.POST, request.FILES, instance=applicants)
                if form.is_valid():
                    form.save()
                    messages.success(request, 'Info Updated')
                    return HttpResponseRedirect(request.META["HTTP_REFERER"])
                else:
                    messages.warning(request, form.errors)
                    return HttpResponseRedirect(request.META["HTTP_REFERER"])
            else:
                form= ApplicantProfileForm(instance=applicants)
        else:
            return redirect('error_page')
        return render(request, 'users/profile_settings.html', {'data':data, 'applicants':applicants, 'form':form})
    except ApplicantProfile.DoesNotExist:
        return render(request, 'users/profile_settings.html')
    

def noProfile(request):
    return render(request, 'users/crud_users/non_ready/not_ready.html')


##################STUDIES ###################
@login_required
@notApplicant
def ShowEducation(request):
    studies = Education.objects.filter(student=request.user)
    if request.method== 'POST':
        form = EducationForm(request.POST)
        
        if form.is_valid():
            education = form.save(commit=False)
            education.student= request.user
            education.save()
            return redirect(request.META['HTTP_REFERER'])
    else:
        form = EducationForm()
    

    return render(request, 'users/info/show_education.html', {'studies':studies, 'form':form})


class UpdateEducation(UpdateView):
    model = Education
    template_name= 'users/info/update_studies.html'
    form_class= EducationForm
    
    def get_success_url(self):
        return reverse('show_education')


class EducationView(generic.DetailView):
    model= Education
    template_name= 'users/info/detail_studies.html'


class DeleteEdu(generic.DeleteView):
    template_name= 'users/info/delete_edu.html'
    queryset= Education.objects.all()
    def get_success_url(self):
        return reverse('show_education')


##### WorkExperience #######

@login_required
@notApplicant
def ShowExperience(request):
    work = Experience.objects.filter(owner=request.user)
    if request.method== 'POST':
        form = ExperienceForm(request.POST, request.FILES)
        
        if form.is_valid():
            experience = form.save(commit=False)
            experience.owner= request.user
            experience.save()
            return redirect(request.META['HTTP_REFERER'])
    else:
        form = ExperienceForm()
    

    return render(request, 'users/info/work/show_work.html', {'work':work, 'form':form})






class UpdateExperience(UpdateView):
    model = Experience
    template_name= 'users/info/work/edit_experience.html'
    form_class= ExperienceForm
    
    def get_success_url(self):
        return reverse('show_experience')


class ViewExperience(generic.DetailView):
    model= Experience
    template_name= 'users/info/work/detail_experience.html'


class DeleteExperience(generic.DeleteView):
    template_name= 'users/info/work/delete_experience.html'
    queryset= Experience.objects.all()
    def get_success_url(self):
        return reverse('show_experience')



##### END EXPERIENCE ##############






@login_required
def P_settings(request, pk):
    data = User.objects.get(id=pk)
    #applicant= ApplicantProfile.objects.get(owner__id=pk)

    #if request.user.is_authenticated and request.user == data:
        #if request.method == 'POST':
            #form2= ApplicantProfileForm(request.POST, request.FILES) #instance=applicant 
            #if form2.is_valid():
                #form2.save()
                #return redirect(request.META['HTTP_REFERER'])
        #else:
            #form2= ApplicantProfileForm()#instance=applicant)
    #else:
        #return redirect('error_page')
    
    context={
    'data':data, #'applicant'#:#applicant,
    #'form2':form2,
    
    }
    return render(request, 'users/settings.html', context)

@login_required
@notApplicant
def EditUser(request, pk):
    data = User.objects.get(id=pk)
    if request.user.is_authenticated and request.user == data:
        if request.method == 'POST':
            form= UserUpdateForm(request.POST, request.FILES, instance=data)
            if form.is_valid():
                form.save()
                messages.success(request, 'Info updated')
                return redirect(request.META['HTTP_REFERER'])
                
                
            
        else:
            form= UserUpdateForm(instance=data)
    else:
        return redirect('error_page')

    context={
    'data':data, 'form':form
    }
    return render(request, 'users/crud_users/update_applicant.html', context)


@login_required
@notApplicant
def Manage_apps(request, pk):
    data = get_object_or_404(User, id=pk)
    if request.user.is_authenticated and request.user == data:
        applications= Applying.objects.filter(sender=pk, submited=True)
    else:
        return redirect('error_page')
    return render(request, 'users/view/applications.html', {'applications':applications})





















@login_required
def Apply_for(request, pk):
    today_date = datetime.date.today()
    
    
    job= get_object_or_404(Jobs, id=pk)
    
    added= bool
    #####USER HAS TO ADD HIS RESUMME FIRST TO APPLY
    if job.save_job.filter(id=request.user.id).exists():
        added=True
    user=User.objects.get(username=request.user)
    review_info= Applying.objects.filter(sender=request.user)
    joo=Applying.objects.filter(sender_id=request.user.id , job_id=job.pk)
    
    #check how many people applied for job of same publisher
    people_applied=Applying.objects.filter(job__publisher=job.publisher, job_id=job.pk)
    if joo:
        return render(request, 'users/error_applied.html', {'job':job})
    else:
        if request.user.is_authenticated and request.user.is_applicant:
            form= ApplyforForm()
            if request.method  ==  'POST':
                form= ApplyforForm(request.POST)
                if form.is_valid():
                    application = form.save(commit=False)
                    application.job= job
                    application.sender= request.user
                    application.submited=True
                    application.save()
                    #send email to publisheer
                    if people_applied.count() <= 1:
                        mail_subject = f"It’s here! The first application for {job.position}"
                        from_email='no-reply@travaii.com'
                        
                        email_message = 'apply_email/applied_for_your_job.html'
                        html_message = render_to_string(email_message, {
                                    'position':job.position,
                                    'publisher':job.publisher.full_name,
                                    'job':job,
                                    'applicant':user.full_name,
                                    'time':today_date,

                                })
                        message = EmailMessage(mail_subject, html_message,from_email, to=[job.publisher.email])
                        message.content_subtype = 'html' # this is required because there is no plain text email version
                        message.send()
                        
                    return render(request, 'users/applied.html', {'job':job})
            else:
                form= ApplyforForm() 
                    
                context= {'form':form, 'job':job, 'review_info':review_info, 'added':added}    
        else:
            return reverse('error_page')
    return render(request, 'application.html', context)