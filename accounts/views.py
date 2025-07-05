# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout
from django.shortcuts import redirect
from .forms import CustomUserCreationForm
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from .forms import StyledAuthenticationForm
from services.models import DiscussionPost, PostReaction


class MyLoginView(LoginView):
    authentication_form = StyledAuthenticationForm
    template_name = 'accounts/login.html'

@never_cache
@login_required
def dashboard(request):
    # your view logic
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
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

def profile(request):
    user = request.user
    # all posts by this user
    posts = DiscussionPost.objects.filter(author=user).order_by('-created_at')
    # all reactions by this user
    reactions = PostReaction.objects.filter(user=user)
    likes_count = reactions.filter(reaction='like').count()
    dislikes_count = reactions.filter(reaction='dislike').count()

    return render(request, 'accounts/profile.html', {
        'posts': posts,
        'likes_count': likes_count,
        'dislikes_count': dislikes_count,
    })

def user_logout(request):
    logout(request)
    return redirect('home')