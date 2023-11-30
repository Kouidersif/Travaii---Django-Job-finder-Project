from dataclasses import fields
from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from main.models import User
from .models import CompanyProfile,Photos_c
# from subscriptions.models import Customer
#Add to a form containing a FileField and change the field names accordingly.
from django.template.defaultfilters import filesizeformat
from django.conf import settings
import os


# class Cancel_SubscForm(forms.ModelForm):
#     class Meta:
#         model= Customer
#         fields = []






class CompanySignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields= ['full_name', 'username', 'email', 'phone_number', 'password1', 'password2']
    def __init__(self, *args, **kwargs):
        super(CompanySignUpForm, self).__init__(*args, **kwargs)
        self.fields['full_name'].widget.attrs['class'] = 'form-control' 
        self.fields['full_name'].widget.attrs['placeholder'] = 'Full Name'
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'Username'
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['placeholder'] = 'email@company.com'
        self.fields['phone_number'].widget.attrs['class'] = 'form-control'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Phone number'
        self.fields['password1'].widget.attrs['class'] = 'form-control' 
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['source'].widget.attrs['class'] = 'form-select'






class UpdateUserForm(UserChangeForm):
    class Meta:
        model = User
        fields= ['full_name', 'username', 'email', 'phone_number']
    def __init__(self, *args, **kwargs):
        super(UpdateUserForm, self).__init__(*args, **kwargs)
        self.fields['full_name'].widget.attrs['class'] = 'form-control' 
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['phone_number'].widget.attrs['class'] = 'form-control'
        self.fields['phone_number'].widget.attrs['placeholder']='xxx-xxx-xx-xx'





class CompanyProfileForm(ModelForm):
    class Meta:
        model = CompanyProfile
        fields= ['company_name', 'industry','co_size','founded','about',  'address',  'city', 'state', 'zip_code',  'website',
        'twitter', 'github', 'facebook', 'company_logo','instagram',  'profile_bg' ]
    def __init__(self, *args, **kwargs):
        super(CompanyProfileForm, self).__init__(*args, **kwargs)
        #added fields to html
        self.fields['company_name'].widget.attrs['class'] = 'form-control form-control-sm text-capitalize'
        self.fields['company_name'].widget.attrs['id'] = 'hireUsFormFirstNameEg1'
        self.fields['company_name'].widget.attrs['placeholder'] = 'Google, Meta...'
        self.fields['company_name'].widget.attrs['name'] = 'hireUsFormNameFirstName'
        ####
        self.fields['industry'].widget.attrs['class'] = 'form-control form-control-sm'
        self.fields['industry'].widget.attrs['placeholder'] = 'Airlines, Banks...'
        self.fields['industry'].widget.attrs['id'] = 'hireUsFormLasttNameEg1'
        self.fields['industry'].widget.attrs['name'] = 'hireUsFormNameLastName'
        ####
        self.fields['founded'].widget.attrs['class'] = 'form-control form-control-sm'
        self.fields['founded'].widget.attrs['placeholder'] = '1998'
        self.fields['founded'].widget.attrs['id'] = 'hireUsFormWorkEmailEg1'
        self.fields['founded'].widget.attrs['name'] = 'hireUsFormNameWorkEmail'
        ####
        self.fields['co_size'].widget.attrs['class'] = 'form-select form-select-sm' 
        
        self.fields['about'].widget.attrs['class'] = 'form-control form-control-sm'
        self.fields['about'].widget.attrs['placeholder'] = 'Talk a bit about your company'
        #second page
        self.fields['address'].widget.attrs['class'] = 'form-control form-control-sm'
        self.fields['address'].widget.attrs['placeholder'] = '1234 East 23th street'
        self.fields['city'].widget.attrs['class'] = 'js-select form-select' 
        self.fields['city'].widget.attrs['id'] = 'city'
        self.fields['city'].widget.attrs['placeholder'] = 'City' 
        self.fields['state'].widget.attrs['class'] = 'js-select form-select'
        self.fields['state'].widget.attrs['placeholder'] = 'State'
        self.fields['zip_code'].widget.attrs['class'] = 'form-control form-control-sm'
        #third page
        self.fields['website'].widget.attrs['class'] = 'form-control'
        self.fields['website'].widget.attrs['type'] = 'url'
        self.fields['website'].widget.attrs['pattern'] = 'https://.*'
        self.fields['website'].widget.attrs['placeholder'] = 'https://'
        self.fields['twitter'].widget.attrs['class'] = 'form-control'
        self.fields['twitter'].widget.attrs['placeholder'] = 'https://'
        self.fields['instagram'].widget.attrs['class'] = 'form-control'
        self.fields['instagram'].widget.attrs['placeholder'] = 'https://'
        self.fields['github'].widget.attrs['class'] = 'form-control'
        self.fields['github'].widget.attrs['placeholder'] = 'https://'
        self.fields['facebook'].widget.attrs['class'] = 'form-control'
        self.fields['facebook'].widget.attrs['placeholder'] = 'https://'
        self.fields['company_logo'].widget.attrs['class'] = 'form-control'
        self.fields['profile_bg'].widget.attrs['class'] = 'form-control'

    def clean_company_name(self):
        company_name= self.cleaned_data['company_name'].capitalize()
        if not company_name:
            raise forms.ValidationError('This company name already exists, if you own this name, Contact us')
        else:
            return company_name
    #facebook validator
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
    def clean_company_logo(self):
        company_logo= self.cleaned_data['company_logo']
        if company_logo and company_logo.size > 5242880:
            get_uploaded_file_size= company_logo.size / (1024.0 * 1024.0)
            raise forms.ValidationError(f'file size should be less than 5MB, your file size is : {round(get_uploaded_file_size, 2)} MB')
        else:
            return company_logo
    def clean_profile_bg(self):
        profile_bg= self.cleaned_data['profile_bg']
        if profile_bg and profile_bg.size > 5242880:
            get_uploaded_file_size= profile_bg.size / (1024.0 * 1024.0)
            raise forms.ValidationError(f'file size should be less than 5MB, your file size is : {round(get_uploaded_file_size, 2)} MB')
        else:
            return profile_bg


        
        
class PhotoForm(ModelForm):
    class Meta:
        model = Photos_c
        fields= ['the_images', 'tag', 'is_public']

    def __init__(self, *args, **kwargs):
        super(PhotoForm, self).__init__(*args, **kwargs)
        #added fields to html
        self.fields['the_images'].widget.attrs['class'] = 'form-control'
        self.fields['tag'].widget.attrs['class'] = 'form-control'
        self.fields['tag'].widget.attrs['placeholder'] = 'Picture at the office'
        self.fields['is_public'].widget.attrs['class'] = 'form-check-input'
    



