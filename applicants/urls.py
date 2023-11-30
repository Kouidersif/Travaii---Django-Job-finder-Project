from django.urls import path
from .views import *
from .decorators import notApplicant




urlpatterns= [
    path('signup/', SignUpApplicant.as_view(), name='sign_up'),
    path('set_up/', ApplicantSetup.as_view(), name='profile_setup'),
    path('profile/not_submited/', noProfile, name='no-profile'),
    path('candidates/', candidates, name='candidates'),
    path('profile/<str:username>/', Profile.as_view(), name='profile'),
    path('update/<int:pk>/', EditUser.as_view(), name='update-user'),
    path('activate/(<uidb64>/<token>/',  activate, name='email_activate'),
    # application
    path('apply_for/apply/<int:pk>/', Apply_for.as_view(), name='apply_for'),
    path('applications/', Manage_apps.as_view(), name='my_applications'), 
    path('security/<int:pk>', P_settings.as_view(), name='applicant_settings'),
    path('about/<int:pk>/', ShowProfile.as_view(), name='applicant_info'),
    # educationn
    path('show_education/', ShowEducation.as_view(), name='show_education'),
    path('edit/education/<int:pk>/', notApplicant(UpdateEducation.as_view()), name='edit_education'),
    path('delete/education/<int:pk>/', notApplicant(DeleteEdu.as_view()), name='delete_education'),
    path('view/<int:pk>/', notApplicant(EducationView.as_view()), name='detail_education'),
    #skills
    path('skills/', ShowSkills.as_view(), name='skills'),
    path('settings/', Account_settings, name='account_settings'),
    path('delete/skill/<int:pk>/', notApplicant(DeleteSkill.as_view()), name='delete_skill'),

    path('view/message/<int:pk>/', CompanyResponse, name='view_message'),

    #experience

    path('show_experience/', ShowExperience.as_view(), name='show_experience'),
    path('edit/experience/<int:pk>/', notApplicant(UpdateExperience.as_view()), name='edit_experience'),
    path('delete/experience/<int:pk>/', notApplicant(DeleteExperience.as_view()), name='delete_experience'),
    path('view/experience/<int:pk>/', notApplicant(ViewExperience.as_view()), name='detail_experience'),

]

