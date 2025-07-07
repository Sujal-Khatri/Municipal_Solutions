import os
from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .models import DiscussionPost, PostReaction, Notice, Report
from .forms import DiscussionPostForm
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from django.conf import settings

@never_cache
def home(request):
    latest_posts = DiscussionPost.objects.order_by('-created_at')[:5]
    return render(request, 'services/home.html', {'latest_posts': latest_posts})
#for search bar
def search(request):
    q = request.GET.get('q', '').strip()
    post_results = DiscussionPost.objects.filter(title__icontains=q) if q else []
    user_model   = get_user_model()
    user_results = user_model.objects.filter(username__icontains=q) if q else []
    return render(request, 'search_results.html', {
        'query': q,
        'post_results': post_results,
        'user_results': user_results,
    })
def dashboard(request):
    # your view logic
    #latest_posts = DiscussionPost.objects.order_by('-created_at')[:5]
    #return render(request, 'services/home.html', {'latest_posts': latest_posts})
    return render(request, 'dashboard.html')
#for notices
def home(request):
    latest_posts = DiscussionPost.objects.order_by('-created_at')[:5]
    notices = Notice.objects.all()[:10]
    return render(request, 'services/home.html', {
        'latest_posts': latest_posts,
        'notices': notices
    })
#gallery work
def _list_gallery(dir_name):
    gallery_dir = os.path.join(settings.BASE_DIR, 'static', 'css', 'img', dir_name)
    files = sorted(f for f in os.listdir(gallery_dir)
                   if f.lower().endswith(('.png','.jpg','.jpeg','.gif')))
    return [f'css/img/{dir_name}/{fname}' for fname in files]

def gallery_left(request):
    # Point at your static folder
    img_dir = os.path.join(settings.BASE_DIR, 'static/css/img/gallery_left')
    files  = sorted(f for f in os.listdir(img_dir)
                    if f.lower().endswith(('.jpg','.jpeg','.png')))
    # build the static paths
    images = [f'css/img/gallery_left/{fname}' for fname in files]
    return render(request, 'gallery_left.html', {'images': images})

def gallery_right(request):
    img_dir = os.path.join(settings.BASE_DIR, 'static/css/img/gallery_right')
    files  = sorted(f for f in os.listdir(img_dir)
                    if f.lower().endswith(('.jpg','.jpeg','.png')))
    images = [f'css/img/gallery_right/{fname}' for fname in files]
    return render(request, 'gallery_right.html', {'images': images})

#for reports
def reports(request):
    all_reports = Report.objects.order_by('-created_at')[:10]
    return render(request, 'services/reports.html', {'reports': all_reports})

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
def service_page(request):
    services = [
        {"title": "Public Construction Department", "desc": "","url": "https://kathmandu.gov.np/wp-content/uploads/2023/02/%E0%A4%B8%E0%A4%BE%E0%A4%B0%E0%A5%8D%E0%A4%B5%E0%A4%9C%E0%A4%A8%E0%A4%BF%E0%A4%95-%E0%A4%A8%E0%A4%BF%E0%A4%B0%E0%A5%8D%E0%A4%AE%E0%A4%BE%E0%A4%A3-%E0%A4%B5%E0%A4%BF%E0%A4%AD%E0%A4%BE%E0%A4%97.pdf"},
        {"title": "Free health services", "desc": "","url": "https://freehealth.kathmandu.gov.np/home/"},
        {"title": "Tax Payment", "desc": "","url": "https://eservice.kathmandu.gov.np/"},
        {"title": "Public Parks", "desc": "Find parks, facilities, and events near you.","url": "https://www.google.com/maps/search/public+parks+in+kathmandu/@27.7181811,85.2762222,27678m/data=!3m1!1e3?entry=ttu&g_ep=EgoyMDI1MDYzMC4wIKXMDSoASAFQAw%3D%3D"},
        {"title": "Education Department", "desc": "","url": "https://kathmandu.gov.np/wp-content/uploads/2023/02/%E0%A4%B6%E0%A4%BF%E0%A4%95%E0%A5%8D%E0%A4%B7%E0%A4%BE-%E0%A4%B5%E0%A4%BF%E0%A4%AD%E0%A4%BE%E0%A4%97-%E0%A4%A8%E0%A4%BE%E0%A4%97%E0%A4%B0%E0%A4%BF%E0%A4%95-%E0%A4%B5%E0%A4%A1%E0%A4%BE%E0%A4%AA%E0%A4%A4%E0%A5%8D%E0%A4%B0.pdf"},
        {"title": "Permit Applications", "desc": "Apply for permits for events, businesses, and construction."}
    ]
    return render(request, 'services/service_page.html', {'services': services})

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

#def home(request):
    #return render(request, 'services/home.html')

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