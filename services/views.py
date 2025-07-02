from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import DiscussionPost, PostReaction
from .forms import DiscussionPostForm
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required

@never_cache

def dashboard(request):
    # your view logic
    return render(request, 'dashboard.html')

def discussions(request):
    posts = DiscussionPost.objects.all().order_by('-created_at')
    return render(request, 'services/discussions.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(DiscussionPost, pk=pk)
     # 🧪 DEBUG PRINT — confirm location field
    print("Location from DB:", post.location)
    user_reaction = None
    if request.user.is_authenticated:
        user_reaction = PostReaction.objects.filter(post=post, user=request.user).first()
    return render(request, 'services/post_detail.html', {
        'post': post,
        'user_reaction': user_reaction
    })

@login_required
def create_post(request):
    if request.method == 'POST':
        form = DiscussionPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user

            # 📍 Capture location properly
            location_val = request.POST.get('location') or request.POST.get('id_location')
            print("📍 Raw location from POST:", location_val)

            if location_val:
                post.location = location_val
            else:
                print("⚠️ Warning: Location field was empty!")

            post.save()
            return redirect('discussions')
    else:
        form = DiscussionPostForm()  # ✅ Fix: initialize form in GET request

    return render(request, 'services/create_post.html', {'form': form})

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(DiscussionPost, id=post_id)
    if request.user == post.author or request.user.is_admin:
        post.delete()
    return redirect('discussions')

def home(request):
    return render(request, 'services/home.html')

@login_required
def like_post(request, pk):
    if not request.user.is_authenticated:
        return redirect('login')

    post = get_object_or_404(DiscussionPost, pk=pk)
    vote = request.POST.get('vote')

    existing = PostReaction.objects.filter(post=post, user=request.user).first()

    if not existing and vote in ['like', 'dislike']:
        PostReaction.objects.create(post=post, user=request.user, reaction=vote)
        if vote == 'like':
            post.likes += 1
        else:
            post.dislikes += 1
        post.save()

    return redirect('post_detail', pk=pk)