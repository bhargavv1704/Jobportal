# core/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/employer/', views.employer_register_view,
         name='employer_register'),
    path('register/jobseeker/', views.jobseeker_register_view,
         name='jobseeker_register'),
    path('dashboard/', views.user_dashboard, name='dashboard'),
    path('jobs/', views.job_list, name='job_list'),
    path('jobs/create/', views.create_job_post, name='create_job_post'),
]
