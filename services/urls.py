from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('discussions/', views.discussions, name='discussions'),
    path('discussions/create/', views.create_post, name='create_post'),
    path('discussions/delete/<int:post_id>/', views.delete_post, name='delete_post'),
]
