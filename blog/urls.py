from django.urls import path 
from . import views




urlpatterns=[
    path('', views.BlogHome, name='blog-home'),
    path('blogging/', views.CreateBlog.as_view(), name='blog-create'),
    path('article/<int:pk>/<str:slug>/', views.BlogDetails, name='blog-detail'),

]