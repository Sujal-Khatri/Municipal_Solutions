from django.urls import path
from .views import MyLoginView, register, user_logout, profile

urlpatterns = [
    path('login/',       MyLoginView.as_view(), name='login'),
    path('logout/',      user_logout,            name='logout'),
    path('register/',    register,               name='register'),
    path('profile/',     profile,                name='profile'),
]