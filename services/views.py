from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import DiscussionPost
from .forms import DiscussionPostForm
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required

@never_cache
@login_required
def dashboard(request):
    # your view logic
    return render(request, 'dashboard.html')

def discussions(request):
    posts = DiscussionPost.objects.all().order_by('-created_at')
    return render(request, 'services/discussions.html', {'posts': posts})

@login_required
def create_post(request):
    if request.method == 'POST':
        form = DiscussionPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('discussions')
    else:
        form = DiscussionPostForm()
    return render(request, 'services/create_post.html', {'form': form})

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(DiscussionPost, id=post_id)
    if request.user == post.author or request.user.is_admin:
        post.delete()
    return redirect('discussions')

def home(request):
    return render(request, 'services/home.html')