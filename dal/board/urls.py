from django.urls import path
from board import views

urlpatterns = [
    # 공지사항 게시판
    path('notice/', views.notice_list, name="notice-list"),
    path('notice/<int:pk>/', views.notice_detail, name="notice-detail"),
    # 콘텐츠 게시판
    path('contents/', views.user_story_list, name="user-story-list"),
    path('contents/<int:pk>/', views.user_story_detail, name="user-story-detail"),
    path('contents/post', views.user_story_form, name="user-story-form"),
]