from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from .forms import EditProfileForm

from .forms import (
    CustomUserCreationForm,
    StyledAuthenticationForm,
    EditProfileForm,
)
from services.models import DiscussionPost, PostReaction


class MyLoginView(LoginView):
    authentication_form = StyledAuthenticationForm
    template_name = 'accounts/login.html'


@never_cache
@login_required
def dashboard(request):
    return render(request, 'dashboard.html')


def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()

    return render(request, 'accounts/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            if user:
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()

    return render(request, 'accounts/login.html', {'form': form})


@login_required
def profile(request):
    user = request.user
    posts = DiscussionPost.objects.filter(author=user).order_by('-created_at')
    reactions = PostReaction.objects.filter(user=request.user).order_by('-id')
    likes_count = reactions.filter(reaction='like').count()
    dislikes_count = reactions.filter(reaction='dislike').count()
    return render(request, 'accounts/profile.html', {
        'posts': posts,
        'reactions': reactions,
        'likes_count': likes_count,
        'dislikes_count': dislikes_count,
    })


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST)
        if form.is_valid():
            u = request.user
            u.email            = form.cleaned_data['email']
            u.phone_number     = form.cleaned_data['phone_number']
            u.profile.location = form.cleaned_data['location']
            u.save()
            u.profile.save()
            return redirect('profile')
    else:
        form = EditProfileForm(initial={
            'email':        request.user.email,
            'phone_number': request.user.phone_number,
            'location':     request.user.profile.location,
        })

    return render(request, 'accounts/edit_profile.html', {
        'form': form
    })

def user_logout(request):
    logout(request)
    return redirect('home')
