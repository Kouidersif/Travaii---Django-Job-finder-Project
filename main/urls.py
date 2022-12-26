from django.urls import path , include
from django.contrib.auth.views import LoginView, LogoutView
from .forms import UserLoginForm
from django.contrib.auth import views as auth_views


from . import views


urlpatterns= [
    path('', views.HomePage, name='home'),
    #path('webhook/', views.stripe_webhook),  # new
    #privacy and Policy
    path('privacy-policy/', views.PrivacyPolicy, name='privacyandpolicy'),


    #authentication
     path('login/', LoginView.as_view(template_name='registration/login.html',
                                                form_class=UserLoginForm), name='log_in'),
    path('logout/', LogoutView.as_view(next_page='home'), name='log_out' ),
    #delete User
    path('account/delete/<int:pk>/', views.DeleteUser, name='delete_user'),
    path('account/activate/', views.ConfirmEmailPage, name='email_confirm'),
    #error page
    path('permission/', views.no_permission, name='error_page'),
    ##Password Reset
    path('reset-pwd/', auth_views.PasswordResetView.as_view(template_name='password_reset/enter_email.html'),name='reset_password'),
    path('email-sent/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset/email_sent.html'), name='password_reset_done'),
    path('reset-pwd/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset/new_pwd_form.html'), name='password_reset_confirm'),
    path('reset-pwd/completed/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset/pwd_changed_complete.html'), name='password_reset_complete'),
    ##change pwd
    path('change-pwd', views.PwdChange.as_view(), name='change_pwd'),
    path('succesfully', views.Successpwd, name='changed'),
    # job
    path('detail/<int:pk>/', views.DetailJob, name='detail_job' ),
    path('delete/<int:pk>/', views.DeleteJob.as_view(), name='delete_job' ),
    path('update/<int:pk>/', views.UpdateJob.as_view(), name='update_job'),
    path('action/<int:pk>/', views.UpdateStatus.as_view(), name='status'),
    path('save_job/<int:id>/', views.SaveJob, name='save_job'),
    path('jobs/category/<int:pk>/', views.Category_list, name='category_list'),
    path('post/', views.CreateJob, name='create_job' ),
    path('all/', views.DisplayJobs, name='alljobs' ),
    path('category/', views.CategoryView, name='category'),
    path('applyList/', views.ApplyList, name='apply_list'),
    path('contact/', views.Contact, name='contact'),
    path('search/', views.Search_for, name='search_for'),
    path('test/', views.Test, name='test_app'),
    path('trial/', views.CreateTrial, name='create_trial'),

]
