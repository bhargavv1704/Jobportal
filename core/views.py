# core/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .forms import EmployerSignUpForm, JobSeekerSignUpForm, JobPostForm
from .models import JobPost, User


def home(request):
    return render(request, 'core/home.html')


def employer_register_view(request):
    if request.method == 'POST':
        form = EmployerSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('create_job_post')
    else:
        form = EmployerSignUpForm()
    return render(request, 'core/register.html', {'form': form, 'role': 'Employer'})


def jobseeker_register_view(request):
    if request.method == 'POST':
        form = JobSeekerSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('job_list')
    else:
        form = JobSeekerSignUpForm()
    return render(request, 'core/register.html', {'form': form, 'role': 'Job Seeker'})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            # Role-based redirection
            if hasattr(user, 'role'):
                if user.role == 'employer':
                    return redirect('create_job_post')
                else:
                    return redirect('job_list')
            else:
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'core/login.html', {'form': form})


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')


@login_required
def create_job_post(request):
    if request.user.role != 'employer':
        return HttpResponseForbidden("Only employers can post jobs.")

    if request.method == 'POST':
        form = JobPostForm(request.POST)
        if form.is_valid():
            job_post = form.save(commit=False)
            job_post.employer = request.user
            job_post.save()
            return redirect('job_list')
    else:
        form = JobPostForm()

    return render(request, 'core/create_job_post.html', {'form': form})


def job_list(request):
    jobs = JobPost.objects.all().order_by('-created_at')
    return render(request, 'core/job_list.html', {'jobs': jobs})


@login_required
def user_dashboard(request):
    if request.user.role == 'employer':
        job_posts = JobPost.objects.filter(employer=request.user)
        context = {
            'job_posts': job_posts,
            'user_role': 'employer'
        }
    else:
        context = {
            'user_role': 'jobseeker'
        }
    return render(request, 'core/dashboard.html', context)
