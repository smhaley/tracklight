from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='track_light_home'),
    path('about/', views.about, name='track_light_about'),
    path('contact/', views.contact, name='track_light_contact'),
]
