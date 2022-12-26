from django.forms import ModelForm
from .models import *
from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.forms import AuthenticationForm
from .models import User

class PwdChangingForm(PasswordChangeForm):
    class Meta:
        model = User
        fields = ['old_password', 'new_password1', 'new_password2']
    def __init__(self, *args, **kwargs):
        super(PwdChangingForm, self).__init__(*args, **kwargs)
        self.fields['old_password'].widget.attrs['class']= 'form-control'
        self.fields['old_password'].widget.attrs['placeholder']= 'Enter Current password'
        self.fields['new_password1'].widget.attrs['class']= 'form-control'
        self.fields['new_password1'].widget.attrs['placeholder']= 'Enter New password'
        self.fields['new_password2'].widget.attrs['class']= 'form-control'
        self.fields['new_password2'].widget.attrs['placeholder']= 'Confirm New password'



class UserLoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields= ['username', 'password']
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'Username'
        self.fields['password'].widget.attrs['class'] = 'form-control'
        self.fields['password'].widget.attrs['placeholder'] = 'Password'




class JobForm(ModelForm):
    class Meta:
        model = Jobs
        fields= ['position', 'job_category','job_type', 'num_people', 'job_shift', 'work_from', 'description','salary_from','salary_to','salary_currency','interview_type', 'is_published']
        widgets= {
        'position': forms.TextInput(attrs={'placeholder':'Customer support representative'}),
        'num_people': forms.TextInput(attrs={'type':'number'}),
        'description': forms.Textarea(attrs={'placeholder':'Requirements or experience needed'}),
        
        
        } 
    def __init__(self, *args, **kwargs):
        super(JobForm, self).__init__(*args, **kwargs)
        self.fields['position'].widget.attrs['class']= 'form-control'
        self.fields['work_from'].widget.attrs['class']= 'form-select'
        self.fields['num_people'].widget.attrs['class']= 'form-control'
        self.fields['num_people'].widget.attrs['placeholder']= 'How many people needed for this job?'
        self.fields['job_category'].widget.attrs['class']= 'js-select form-select form-select-lg'
        self.fields['job_category'].widget.attrs['placeholder']= 'Select category'
        self.fields['job_type'].widget.attrs['class']= 'form-select'
        self.fields['job_shift'].widget.attrs['class']= 'form-select'
        self.fields['salary_from'].widget.attrs['type'] = 'number'
        self.fields['salary_from'].widget.attrs['class']= 'form-control'
        self.fields['salary_from'].widget.attrs['placeholder']= 'from'
        self.fields['salary_to'].widget.attrs['type'] = 'number'
        self.fields['salary_to'].widget.attrs['class']= 'form-control'
        self.fields['salary_to'].widget.attrs['placeholder']= 'to'
        self.fields['salary_currency'].widget.attrs['class']= 'form-select'
        #self.fields['pay_per'].widget.attrs['class']= 'form-select'
        self.fields['interview_type'].widget.attrs['class']= 'form-select'
        self.fields['description'].widget.attrs['class']= 'form-control'
        self.fields['is_published'].widget.attrs['class']='form-check-input'




class ContactForm(ModelForm):
    class Meta:
        model = ContactUs
        fields= '__all__'
    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.fields['full_name'].widget.attrs['class'] = 'form-control'
        self.fields['title'].widget.attrs['class'] = 'form-control'
        self.fields['message'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['class'] = 'form-control'



class EditApplyForm(ModelForm):
    class Meta:
        model = Applying
        fields= ['request']
        widgets= {
        'request': forms.Select(attrs={'class':'form-select'}),
        }



class DateInput(forms.DateInput):
    input_type= 'date'


class EducationForm(ModelForm):
    widgets={'started': DateInput()}
    widgets={'end': DateInput()}
    class Meta:
        model = Education
        fields= ['degree', 'University','speciality', 'extra_info', 'started', 'end' ]
    def __init__(self, *args, **kwargs):
        super(EducationForm, self).__init__(*args, **kwargs)
        self.fields['degree'].widget.attrs['class']= 'form-control'
        self.fields['University'].widget.attrs['class']= 'form-control'
        self.fields['speciality'].widget.attrs['class']= 'form-control'
        self.fields['extra_info'].widget.attrs['class']= 'form-control'
        self.fields['started'].widget.attrs['class']= 'form-control'
        self.fields['end'].widget.attrs['class']= 'form-control'


class SkillsForm(ModelForm):
    class Meta:
        model = Skills
        fields = ['skill']
    def __init__(self, *args, **kwargs):
        super(SkillsForm, self).__init__(*args, **kwargs)
        self.fields['skill'].widget.attrs['class']='form-control'

class ExperienceForm(ModelForm):
    class Meta:
        model = Experience
        fields= ['title','co_location','company','still_working', 'industry', 'about_role', 'company_pic_exp', 'started', 'end']
    def __init__(self, *args, **kwargs):
        super(ExperienceForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs['class']='form-control'
        self.fields['title'].widget.attrs['placeholder']='Senior IOS Developper'
        self.fields['co_location'].widget.attrs['class']='form-control'
        self.fields['co_location'].widget.attrs['placeholder']='City or State'
        self.fields['company_pic_exp'].widget.attrs['class']='form-control'
        self.fields['company'].widget.attrs['class']='form-control'
        self.fields['company'].widget.attrs['placeholder']='Company name'
        self.fields['industry'].widget.attrs['class']='form-control'
        self.fields['industry'].widget.attrs['placeholder']='Technology'
        self.fields['still_working'].widget.attrs['class']='form-select'
        self.fields['about_role'].widget.attrs['class']='form-control'
        self.fields['about_role'].widget.attrs['placeholder']='Tell everyone about the impact you made in previous companies'
        self.fields['started'].widget.attrs['class']= 'form-control'
        self.fields['end'].widget.attrs['class']= 'form-control'


