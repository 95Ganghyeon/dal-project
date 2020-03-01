from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from product.views import get_paginator
from user.models import *
from .models import *
from .forms import UserStroyForm

def notice_list(request):
    return render(request, "notice_list.html", context={})


def notice_detail(request, pk):
    return render(request, "notice_detail.html", context={})
    


def user_story_list(request):
    return render(request, "user_story_list.html", context={})

def user_story_detail(request, pk):
    user_story = get_object_or_404(User_story, id=pk)

    # 조회수 증가
    user_story.hits += 1
    user_story.save()

    if request.user.is_active:
        # 로그인한 경우 좋아요 체크 유무 알려주기
        is_like = user_story.likes.filter(id=request.user.id).exists()
        return render(request, "user_story_detail.html", context={'user_story': user_story, 'is_like': is_like})
    else:
        return render(request, "user_story_detail.html", context={'user_story': user_story})    

# 사연 작성 페이지
def user_story_form(request):
    form = UserStroyForm(label_suffix='')

    if request.method == 'POST':
        user = request.user
        form = UserStroyForm(request.POST, request.FILES)

        if form.is_valid():
            form.save(commit=False)
            form.instance.user = request.user
            form.save()
        
        return HttpResponse('success')

    return render(request, "user_story_form.html", context={'form': form})


# 콘텐츠 좋아요
def check_like(request, pk):
    user = request.user
    user_story = User_story.objects.get(id=pk)

    if user_story.likes.filter(id=user.id).exists():
        # 이미 좋아요 체크한 경우 -> 비활성화
        user_story.likes.remove(request.user)
    else:
        # 좋아요 활성화
        user_story.likes.add(request.user)
    
    return HttpResponse(user_story.total_likes)
