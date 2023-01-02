from django.forms import ModelForm
from django.contrib.auth.forms import AuthenticationForm
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from main.models import *
from .models import *
from django.core.exceptions import ValidationError

from datetime import date

class DateInput(forms.DateInput):
    input_type= 'date'


class NewsLetterForm(ModelForm):
    class Meta:
        model = NewsLetter
        fields= '__all__'
    def __init__(self, *args, **kwargs):
        super(NewsLetterForm, self).__init__(*args, **kwargs)
        self.fields['email_field'].widget.attrs['class'] = 'form-control'
        self.fields['email_field'].widget.attrs['type'] = 'email'
        self.fields['email_field'].widget.attrs['placeholder'] = 'Enter your email'
        self.fields['job_category'].widget.attrs['class'] = 'js-select form-select-md'
        self.fields['job_category'].widget.attrs['placeholder'] = 'choose your dream job'
        



class ApplicantProfileForm(ModelForm):
    class Meta:
        widgets={'birthday': DateInput()}
        model = ApplicantProfile
        fields= ['city','state','languages','linkedin','github','p_website',
        'facebook','instagram','desired_job','birthday',
        'applicant_cv', 'is_public', 'about', 'profile_pic','desired_industry', 'desired_job_type', 'desired_shift']
    def __init__(self, *args, **kwargs):
        super(ApplicantProfileForm, self).__init__(*args, **kwargs)
        self.fields['profile_pic'].widget.attrs['class'] = 'form-control'
        self.fields['profile_pic'].widget.attrs['id'] = 'basicFormFile'
        self.fields['profile_pic'].widget.attrs['type'] = 'file'
        self.fields['city'].widget.attrs['class'] = 'js-select form-select'
        self.fields['city'].widget.attrs['placeholder'] = 'City'
        self.fields['state'].widget.attrs['class'] = 'js-select form-select'
        self.fields['state'].widget.attrs['placeholder'] = 'State'
        self.fields['languages'].widget.attrs['class'] = 'js-select form-select'
        self.fields['languages'].widget.attrs['placeholder'] = 'Select languages'
        self.fields['desired_industry'].widget.attrs['class'] = 'js-select form-select'
        self.fields['desired_industry'].widget.attrs['placeholder'] = 'Select industry'
        self.fields['desired_job_type'].widget.attrs['class'] = 'js-select form-select'
        self.fields['desired_shift'].widget.attrs['class'] = 'js-select form-select'
        self.fields['linkedin'].widget.attrs['class'] = 'form-control'
        self.fields['linkedin'].widget.attrs['placeholder'] = 'https://'
        self.fields['github'].widget.attrs['class'] = 'form-control'
        self.fields['github'].widget.attrs['placeholder'] = 'https://'
        self.fields['p_website'].widget.attrs['class']= 'form-control'
        self.fields['p_website'].widget.attrs['placeholder']= 'https://'
        self.fields['facebook'].widget.attrs['class'] = 'form-control'
        self.fields['facebook'].widget.attrs['placeholder'] = 'https://'
        self.fields['instagram'].widget.attrs['class']= 'form-control'
        self.fields['instagram'].widget.attrs['placeholder'] = 'https://'
        self.fields['desired_job'].widget.attrs['class'] = 'js-select form-select'
        self.fields['desired_job'].widget.attrs['placeholder'] = 'Add desired job'
        self.fields['birthday'].widget.attrs['class'] = 'form-control form-control-sm'
        #self.fields['birthday'].widget.attrs['type'] = 'date'
        self.fields['applicant_cv'].widget.attrs['class']='form-control'
        self.fields['is_public'].widget.attrs['class']= 'js-select form-select'
        self.fields['about'].widget.attrs['class'] = 'form-control'
        self.fields['about'].widget.attrs['placeholder'] = 'Let companies know about your carrer and what you are capable of'
    def clean_birthday(self):
        birthday = self.cleaned_data['birthday']
        today = date.today()
        age= today.year - birthday.year - ((today.month, today.day) < (birthday.month, birthday.day))
        if age >= 18:
            return birthday
        else:
            raise ValidationError("You must be over 18")

        
        
        
        
    def clean_applicant_cv(self):
        applicant_cv = self.cleaned_data['applicant_cv']
        if applicant_cv and applicant_cv.size > 5242880:
            get_uploaded_file_size= applicant_cv.size / (1024.0 * 1024.0)
            raise forms.ValidationError(f'file size should be less than 5MB, your file size is : {round(get_uploaded_file_size, 2)} MB')
        else:
            return applicant_cv

    def clean_profile_pic(self):
        profile_pic = self.cleaned_data['profile_pic']
        if profile_pic and profile_pic.size > 5242880:
            get_uploaded_file_size= profile_pic.size / (1024.0 * 1024.0)
            raise forms.ValidationError(f'file size should be less than 5MB, your file size is : {round(get_uploaded_file_size, 2)} MB')
        else:
            return profile_pic

    def clean_facebook(self):
        facebook = self.cleaned_data['facebook']
        if facebook and 'facebook.com' not in facebook:
            raise forms.ValidationError('link must contain facebook.com')
        else:
            return facebook
    #Twitter Validator
    def clean_twitter(self):
        twitter = self.cleaned_data['twitter']
        if twitter and 'twitter.com' not in twitter:
            raise forms.ValidationError('link must contain twitter.com')
        else:
            return twitter
    #Instagram Validator
    def clean_instagram(self):
        instagram = self.cleaned_data['instagram']
        if instagram and 'instagram.com' not in instagram:
            raise forms.ValidationError('link must contain instagram.com')
        else:
            return instagram
    #Github Validator
    def clean_github(self):
        github = self.cleaned_data['github']
        if github and 'github.com' not in github:
            raise forms.ValidationError('link must contain github.com')
        else:
            return github

















class UserUpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields= ['full_name', 'username', 'email',  'gender', 'phone_number']

    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = 'Username'
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['full_name'].widget.attrs['class'] = 'form-control'
        self.fields['full_name'].widget.attrs.update(placeHolder='Ex. Mark Smith')
        self.fields['email'].widget.attrs.update(placeHolder='Ex. smith123@gmail.com')
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['gender'].widget.attrs['class'] = 'form-select'
        self.fields['phone_number'].widget.attrs['class']= 'js-input-mask form-control'
        self.fields['phone_number'].widget.attrs['id']= 'phoneLabel'
        self.fields['phone_number'].widget.attrs['name']= 'phone'
        self.fields['phone_number'].widget.attrs['placeholder']='xxx-xxx-xx-xx'


class ApplicantSignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields= ['full_name', 'username', 'email',  'gender', 'password1', 'password2', 'source', 'phone_number']

    def __init__(self, *args, **kwargs):
        super(ApplicantSignUpForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        #self.fields['username'].widget.attrs['name'] = 'username'
        #self.fields['username'].widget.attrs['id'] = 'validationFormUsernameLabel'
        self.fields['username'].widget.attrs['placeholder'] = 'Username'
        #self.fields['username'].widget.attrs['required data-msg'] = 'Please enter your username.'
        #PWD
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        #self.fields['password1'].widget.attrs['name'] = 'newPassword'
        self.fields['password1'].widget.attrs['type'] = 'password'
        #self.fields['password1'].widget.attrs['id'] = 'validationFormNewPasswordLabel'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        #self.fields['password1'].widget.attrs['required data-msg'] = 'Please enter your Password.'
        #PWD2
        self.fields['password2'].widget.attrs['class'] = 'form-control'
        #self.fields['password2'].widget.attrs['name'] = 'newPassword'
        self.fields['password2'].widget.attrs['type'] = 'password'
        #self.fields['password2'].widget.attrs['id'] = 'validationFormCurrentPasswordLabel'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
        #self.fields['password2'].widget.attrs['required data-msg'] = 'Please enter your Password.'
        #email
        self.fields['email'].widget.attrs['class'] = 'form-control'
        #self.fields['email'].widget.attrs['name'] = 'email'
        self.fields['email'].widget.attrs['type'] = 'email'
        #self.fields['email'].widget.attrs['id'] = 'validationFormEmailLabel'
        self.fields['email'].widget.attrs['placeholder'] = 'name@example.com'
        #self.fields['email'].widget.attrs['required data-msg'] = 'Please enter your Email.'
        #name
        self.fields['full_name'].widget.attrs['class'] = 'form-control'
        #self.fields['full_name'].widget.attrs['name'] = 'lastName'
        self.fields['full_name'].widget.attrs['type'] = 'text'
        #self.fields['full_name'].widget.attrs['id'] = 'validationFormLastNameLabel'
        self.fields['full_name'].widget.attrs['placeholder'] = 'Full Name'
        #self.fields['full_name'].widget.attrs['required data-msg'] = 'Please enter your Full Name.'
        #gender
        self.fields['gender'].widget.attrs['class'] = 'form-select'
        self.fields['gender'].widget.attrs['placeholder'] = 'Gender'

        self.fields['source'].widget.attrs['class'] = 'form-select'
        self.fields['source'].widget.attrs['placeholder'] = 'source'
        self.fields['phone_number'].widget.attrs['class']= 'js-input-mask form-control'
        self.fields['phone_number'].widget.attrs['placeholder']='xxx-xxx-xx-xx'
        
    





class ApplyforForm(ModelForm):
    class Meta:
        model= Applying
        fields= ['about', 'experience', 'expected_salary', 'expected_salary_currency']

    def __init__(self, *args, **kwargs):
        super(ApplyforForm, self).__init__(*args, **kwargs)
        self.fields['about'].widget.attrs['class'] = 'form-control'
        self.fields['about'].widget.attrs['placeholder'] = 'Let the employeer know how excited you are for this role and what advatages you can offer the company'
        self.fields['experience'].widget.attrs['class'] = 'form-select'
        self.fields['expected_salary'].widget.attrs['class'] = 'form-control'
        self.fields['expected_salary_currency'].widget.attrs['class'] = 'form-control'
        self.fields['expected_salary'].widget.attrs['placeholder'] = 'Optional - set your salary expectations for this role'




class Feedback(ModelForm):
    class Meta:
        model = Delete_account_Feedback
        fields= ['the_reason', 'reason_txt']

