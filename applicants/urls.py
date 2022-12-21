from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from .decorators import notApplicant
urlpatterns= [
    path('signup/', views.Signup_as_applicant, name='sign_up'),
    path('set_up/', views.Applicant_Setup, name='profile_setup' ),
    path('profile/not_submited/', views.noProfile, name='no-profile' ),
    path('candidates/', views.candidates, name='candidates'),
    path('profile/<str:username>/', views.Profile, name='profile'),
    path('update/<int:pk>/', views.EditUser, name='update-user'),
    path('activate/(<uidb64>/<token>/',  
        views.activate, name='email_activate'),
    #wishlist
    path('applicant_cv/', views.Applicant_cv, name='my_cv'),
    #application
    path('apply_for/apply/<int:pk>/', views.Apply_for, name='apply_for'),
    path('applications/<int:pk>/', views.Manage_apps, name='my_applications'), 
    path('security/<int:pk>', views.P_settings, name='applicant_settings' ),
    path('about/<int:pk>/', views.ShowProfile, name='applicant_info'),
    ##educationn
    path('education/', views.Studies, name='education'),
    path('show_education/', views.ShowEducation, name='show_education'),
    path('edit/education/<int:pk>/', notApplicant(views.UpdateEducation.as_view()), name='edit_education'),
    path('delete/education/<int:pk>/', notApplicant(views.DeleteEdu.as_view()), name='delete_education'),
    path('view/<int:pk>/', notApplicant(views.EducationView.as_view()), name='detail_education'),
    #skills
    path('skills/', views.ShowSkills, name='skills'),
    path('settings/', views.Account_settings, name='account_settings'),
    path('delete/skill/<int:pk>/', notApplicant(views.DeleteSkill.as_view()), name='delete_skill'),

    #experience

    path('show_experience/', views.ShowExperience, name='show_experience'),
    path('edit/experience/<int:pk>/', notApplicant(views.UpdateExperience.as_view()), name='edit_experience'),
    path('delete/experience/<int:pk>/', notApplicant(views.DeleteExperience.as_view()), name='delete_experience'),
    path('view/experience/<int:pk>/', notApplicant(views.ViewExperience.as_view()), name='detail_experience'),


    #email activate



]

