from django.urls import path
from . import views
from .decorators import notLogged
urlpatterns= [
    #path('', views.HomePage.as_view(), name='jobs_list'),
    path('signup/', views.Signup_as_company, name='sign_up_company'),
    path('setup/', views.Company_setup, name='company_setup'),
    path('profile/<int:pk>/', views.Setup_Profile, name='company_Profile'),
    path('update_profile/<int:pk>/', views.UpdateCompany, name='company_update'),
    #path('login/', LoginView.as_view(), name='log_in_company' ),
    path('application/', views.view_application, name='view_application'),
    path('p/<int:pk>/', views.U_Profile, name='u_profile'),
    path('manage/subscription/', views.manage_subscription, name='manage-subscription'),
    path('manage/', views.Apps_jobs, name='manage_jobs'),
    path('assets/', views.Side_Bar),
    path('account/', views.account_categories, name='account_categories'),
    #path('cancel_sub/<int:pk>/', views.Cancel_sub, name='cancelsub'),
    #add PHotos
    path('add/photos/', views.PostPhotos, name='add_photos'),
    path('photos/view/<int:pk>/', views.View_all, name='view_company_photos'),
    path('photo/<int:pk>/delete/', views.DeletePhotos, name='delete_photos'),
    path('photo/edit/privacy/<int:pk>/', views.Edit_photo_privacy, name='change_photo_privacy'),
    #deletepaymethod
    path('delete/<str:card_id>/', views.Delete_PM, name='payment_method_delete'),
    path('default/card/<str:card_id>/', views.Make_card_default, name='card_default'),
    #subscription managin:
    path('update/<str:subscription_id>/', views.Cancel_sub_or_reactivate, name='reactivate_or_cancel'),
    ## save PRofiles
    path('save_profile/<int:id>/', views.SaveApplicant, name='save_applicant_profile'),
    path('saved_profiles/', views.Saved_Profiles, name='saved_profiles'),

]