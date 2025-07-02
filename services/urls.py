from django.urls import path
from .views import service_page
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('discussions/', views.discussions, name='discussions'),
    path('discussions/create/', views.create_post, name='create_post'),
    path('discussions/<int:pk>/', views.post_detail, name='post_detail'),
    path('discussions/<int:pk>/react/', views.like_post, name='like_post'),
    path('discussions/delete/<int:post_id>/', views.delete_post, name='delete_post'),
    path('services/', service_page, name='service_page'),
]
