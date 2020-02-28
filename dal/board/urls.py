from django.urls import path
from board import views

urlpatterns = [
    path('notice/<int:pk>/', views.notice_detail, name="notice-detail"),
    path('contents/<int:pk>/', views.user_story_detail, name="user-story-detail"),
]