from django.urls import path
from .views import service_page
from services import views as service_views
from services.views  import tax_form, esewa_success, esewa_failure
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('discussions/', views.discussions, name='discussions'),
    path('discussions/create/', views.create_post, name='create_post'),
    path('discussions/<int:pk>/', views.post_detail, name='post_detail'),
    path('discussions/<int:pk>/react/', views.like_post, name='like_post'),
    path('discussions/delete/<int:post_id>/', views.delete_post, name='delete_post'),
    path('search/', service_views.search, name='search'),
    path('services/', service_page, name='service_page'),
    path('reports/', views.reports, name='reports'),
    path('gallery/left/', views.gallery_left, name='gallery_left'),
    path('gallery/right/', views.gallery_right, name='gallery_right'),
    path('tax/form/',               views.tax_form,           name='tax_form'),
    path('tax/<int:pk>/receipt/',   views.tax_receipt_upload, name='tax_receipt_upload'),
    path('tax/<int:pk>/detail/',    views.tax_detail,         name='tax_detail'),
    path('tax/form/', views.tax_form, name='tax_form'),
    path('tax/esewa/redirect/', views.esewa_redirect, name='esewa_redirect'),
    path('tax/form/',    tax_form,       name='tax_form'),
    path('tax/success/', esewa_success,  name='esewa_success'),
    path('tax/failure/', esewa_failure,  name='esewa_failure'),
]
