from django.urls import path 
from . import views
from django.conf import settings

urlpatterns=[
    path('', views.subscribe, name='subscription'),
    #path('join', views.reactivate_sub, name='re-activate'),
    path('test/add/', views.add_Card, name='add_card'),
    path('checkout', views.checkout, name='checkout'),
    path('success', views.success, name='success'),
    path('cancel', views.cancel, name='cancel'),
    #path('auth/settings', views.U_ettings, name='settings'),
    #path('updateaccounts', views.updateaccounts, name='updateaccounts'),
    path('webhook/', views.stripe_webhook),
    path('yearly/', views.yearly, name='yearly'),
    path('ss/', views.customer_portal, name='s'),
    path('summary/', views.ShowTotal_before_update, name='show_total'),
    path('changed', views.Update_subscription, name='update_sub'),
    path('test/clock/', views.TestClock, name='testclock'),
    path('clock/tested/', views.Advance_time, name='clock test'),
]