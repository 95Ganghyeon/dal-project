from django.urls import path
from user import views

urlpatterns = [
    path('profile/',views.profile,name='profile')
]
