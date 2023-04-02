from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import HttpResponse
from .forms import *
from django.views import generic
from main.models import *
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.views import generic
from main.forms import *
from .filtering import *
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.conf import settings
from .decorators import notApplicant
from .email_token import TokenGenerator
from .email_token import account_activation_token
from company.decorators import notLogged
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site  
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode  
from django.contrib.auth import get_user_model
from django.template import Context
from .mixins import MustbeUnauthenticated, ApplicantsAccess
from .tasks import inform_company


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



class SignUpApplicant(MustbeUnauthenticated, generic. FormView):
    form_class = ApplicantSignUpForm
    template_name = 'users/registration/signup.html'
    def form_valid(self, form):
        user = form.save()
        user.is_applicant=True
        user.save()
        new_user= authenticate(
            username= form.cleaned_data['username'],
            password= form.cleaned_data['password1']
        )
        login(self.request, new_user)
        return super().form_valid(form)
    def get_success_url(self) -> str:
        return reverse("home")






class Profile(ApplicantsAccess, generic. DetailView):
    template_name = 'users/profile_page.html'
    model = User
    context_object_name = "user"

    def get_object(self):
        return User.objects.get(username=self.kwargs['username'])
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.object
        context['applicants'] = ApplicantProfile.objects.filter(owner=user)
        context['study'] = Education.objects.filter(student=user)
        context['myskills'] = Skills.objects.filter(owner=user)
        context['experience'] = Experience.objects.filter(owner=user)
        return context



@login_required
@notApplicant
def Account_settings(request):
    return render(request, 'users/account_categories.html')




class ShowSkills(ApplicantsAccess, generic. FormView):
    template_name = 'users/info/skills/show_skills.html'
    form_class = SkillsForm
    def get(self, request):
        skills = Skills.objects.filter(owner=request.user)
        return render(request, 'users/info/skills/show_skills.html', {'skills':skills, 'form':self.form_class})
    def form_valid(self, form) -> HttpResponse:
        education = form.save(commit=False)
        education.owner= self.request.user
        education.save()
        return redirect(self.request.META['HTTP_REFERER'])



class DeleteSkill(ApplicantsAccess, generic.DeleteView):
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







class ApplicantSetup(ApplicantsAccess ,generic. FormView):
    form_class = ApplicantProfileForm
    template_name = 'users/applicant_set_up.html'
    def form_valid(self, form):
        applicant = form.save(commit=False)
        applicant.owner = self.request.user
        applicant.save()
        applicant.submited = True
        applicant.save()
        return redirect('email_confirm')











class ShowProfile(ApplicantsAccess, generic.UpdateView):
    model = ApplicantProfile
    form_class = ApplicantProfileForm
    template_name = 'users/profile_settings.html'
    
    def get_object(self):
        return ApplicantProfile.objects.get(owner__id=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["applicants"] = ApplicantProfile.objects.get(owner=self.kwargs["pk"])
        return context
    
    def get_success_url(self) -> str:
        messages.success(self.request, "Info Updated")
        return reverse("applicant_info", args=[self.kwargs["pk"]])







def noProfile(request):
    return render(request, 'users/crud_users/non_ready/not_ready.html')








##################STUDIES ###################


class ShowEducation(ApplicantsAccess ,generic. FormView):
    form_class = EducationForm
    template_name = 'users/info/show_education.html'

    def form_valid(self, form):
        education = form.save(commit=False)
        education.student= self.request.user
        education.save()
        return redirect(self.request.META['HTTP_REFERER'])
    
    def get(self, request):
        studies = Education.objects.filter(student=request.user)
        return render(request, 'users/info/show_education.html', {'studies':studies, "form":self.form_class})




class UpdateEducation(ApplicantsAccess, generic. UpdateView):
    model = Education
    template_name= 'users/info/update_studies.html'
    form_class= EducationForm
    
    def get_success_url(self):
        return reverse('show_education')


class EducationView(ApplicantsAccess, generic.DetailView):
    model= Education
    template_name= 'users/info/detail_studies.html'


class DeleteEdu(ApplicantsAccess, generic.DeleteView):
    template_name= 'users/info/delete_edu.html'
    queryset= Education.objects.all()
    def get_success_url(self):
        return reverse('show_education')


##### WorkExperience #######


class ShowExperience(ApplicantsAccess ,generic. FormView):
    form_class = ExperienceForm
    template_name = 'users/info/work/show_work.html'

    def form_valid(self, form):
        education = form.save(commit=False)
        education.owner = self.request.user
        education.save()
        return redirect(self.request.META['HTTP_REFERER'])

    def get(self, request):
        work = Experience.objects.filter(owner=request.user)
        return render(request, 'users/info/work/show_work.html', {'work':work, "form":self.form_class})






class UpdateExperience(ApplicantsAccess, generic. UpdateView):
    model = Experience
    template_name= 'users/info/work/edit_experience.html'
    form_class= ExperienceForm
    
    def get_success_url(self):
        return reverse('show_experience')


class ViewExperience(ApplicantsAccess, generic.DetailView):
    model= Experience
    template_name= 'users/info/work/detail_experience.html'


class DeleteExperience(ApplicantsAccess, generic.DeleteView):
    template_name= 'users/info/work/delete_experience.html'
    queryset= Experience.objects.all()
    def get_success_url(self):
        return reverse('show_experience')



##### END EXPERIENCE ##############









class P_settings(ApplicantsAccess , generic. DetailView):
    template_name = 'users/settings.html'
    model = User
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["data"] = User.objects.get(id=self.kwargs["pk"])
        return context





class EditUser(ApplicantsAccess , generic. UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'users/crud_users/update_applicant.html'

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Info updated')
        return redirect(self.request.META['HTTP_REFERER'])
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["data"] = User.objects.get(id=self.kwargs["pk"])
        return context





class Manage_apps(ApplicantsAccess,generic. TemplateView):
    template_name = 'users/view/applications.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["applications"] = Applying.objects.filter(sender=self.request.user, submited=True)
        return context












class Apply_for(ApplicantsAccess ,generic. View):

    def get(self, request, pk):
        added = False
        job = get_object_or_404(Jobs, id=pk)
        review_info= Applying.objects.filter(sender=request.user)
        user_applied = Applying.objects.filter(sender_id=request.user.id , job_id=job.pk)

        if job.save_job.filter(id=request.user.id).exists():
            added = True #refers to jobs saved by User
        
        if user_applied:
            return render(request, 'users/error_applied.html', {'job':job})
        
        context = {"job":job, "form":ApplyforForm(),"review_info":review_info, "added":added}
        return render(request, "application.html", context)
    
    def post(self, request, pk):
        job = get_object_or_404(Jobs, id=pk)
        people_applied=Applying.objects.filter(job__publisher=job.publisher, job_id=job.pk)
        user=User.objects.get(username=request.user)
        form= ApplyforForm(request.POST)

        if form.is_valid():
            application = form.save(commit=False)
            application.job= job
            application.sender= request.user
            application.submited=True
            application.save()
            #notify company :
            if people_applied.count() <= 1:
                inform_company.delay(job.id, user.id)
        return render(request, 'users/applied.html', {'job':job})





