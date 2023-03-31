from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from .decorators import notApplicant
urlpatterns= [
    path('signup/', views.SignUpApplicant.as_view(), name='sign_up'),
    path('set_up/', views.ApplicantSetup.as_view(), name='profile_setup' ),
    path('profile/not_submited/', views.noProfile, name='no-profile' ),
    path('candidates/', views.candidates, name='candidates'),
    path('profile/<str:username>/', views.Profile.as_view(), name='profile'),
    path('update/<int:pk>/', views.EditUser.as_view(), name='update-user'),
    path('activate/(<uidb64>/<token>/',  
        views.activate, name='email_activate'),
    #wishlist
    path('applicant_cv/', views.Applicant_cv, name='my_cv'),
    #application
    path('apply_for/apply/<int:pk>/', views.Apply_for.as_view(), name='apply_for'),
    path('applications/', views.Manage_apps.as_view(), name='my_applications'), 
    path('security/<int:pk>', views.P_settings.as_view(), name='applicant_settings' ),
    path('about/<int:pk>/', views.ShowProfile.as_view(), name='applicant_info'),
    ##educationn
    path('show_education/', views.ShowEducation.as_view(), name='show_education'),
    path('edit/education/<int:pk>/', notApplicant(views.UpdateEducation.as_view()), name='edit_education'),
    path('delete/education/<int:pk>/', notApplicant(views.DeleteEdu.as_view()), name='delete_education'),
    path('view/<int:pk>/', notApplicant(views.EducationView.as_view()), name='detail_education'),
    #skills
    path('skills/', views.ShowSkills.as_view(), name='skills'),
    path('settings/', views.Account_settings, name='account_settings'),
    path('delete/skill/<int:pk>/', notApplicant(views.DeleteSkill.as_view()), name='delete_skill'),

    path('view/message/<int:pk>/', views.CompanyResponse, name='view_message'),

    #experience

    path('show_experience/', views.ShowExperience.as_view(), name='show_experience'),
    path('edit/experience/<int:pk>/', notApplicant(views.UpdateExperience.as_view()), name='edit_experience'),
    path('delete/experience/<int:pk>/', notApplicant(views.DeleteExperience.as_view()), name='delete_experience'),
    path('view/experience/<int:pk>/', notApplicant(views.ViewExperience.as_view()), name='detail_experience'),


    #email activate



]

