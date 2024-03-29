from django.urls import path
from .views import *



urlpatterns= [

    path('', LandingPage, name='CompanyLandingPage'),
    path('signup/', Signup_as_company.as_view(), name='sign_up_company'),
    path('setup/', Company_Setup.as_view(), name='company_setup'),
    path('profile/<int:pk>/', Company_Page.as_view(), name='company_Profile'),
    path('update_profile/<int:pk>/', UpdateCompany.as_view(), name='company_update'),

    path('application/', view_application, name='view_application'),
    path('p/<int:pk>/', RecruiterProfile.as_view(), name='u_profile'),
    path('manage/', Apps_jobs, name='manage_jobs'),
    path('account/', account_categories, name='account_categories'),

    #add PHotos
    path('add/photos/', PostPhotos.as_view(), name='add_photos'),
    path('photos/view/<int:pk>/', ViewPhotos.as_view(), name='view_company_photos'),
    path('photo/<int:pk>/delete/', DeletePhoto.as_view(), name='delete_photos'),
    path('photo/edit/privacy/<int:pk>/', EditPhotoPrivacy.as_view(), name='change_photo_privacy'),
    ## save PRofiles

    path('save_profile/<int:id>/', SaveApplicant, name='save_applicant_profile'),
    path('saved_profiles/', Saved_Profiles, name='saved_profiles'),

]