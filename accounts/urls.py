from django.urls import path
from . import views 
from django.urls import path
from .views import MyLoginView, register, user_logout

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('login/', MyLoginView.as_view(), name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.register, name='register'),
]
