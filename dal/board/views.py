from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from product.views import get_paginator
from user.models import *
from .models import *
from .forms import UserStroyForm
from django.db.models import Case, When, Value, BooleanField, Exists 

# 공지사항 리스트 페이지
def notice_list(request):
    
    query_string = ""

    # 쿼리스트링 생성 for paginator
    if request.META["QUERY_STRING"]:
        for item in request.META["QUERY_STRING"].split("&"):
            if "page" not in item:
                query_string += "&" + item

    if request.GET.get("category") == "entire":
        fixed_notice_list = Notice.objects.all().filter(is_fixed=True)
        notice_list = Notice.objects.all().order_by('-created_at')
    elif request.GET.get("category") == "notice":
        fixed_notice_list = Notice.objects.all().filter(category="notice", is_fixed=True)
        notice_list = Notice.objects.all().filter(category="notice").order_by('-created_at')
    elif request.GET.get("category") == "event":
        fixed_notice_list = Notice.objects.all().filter(category="event", is_fixed=True)
        notice_list = Notice.objects.all().filter(category="event").order_by('-created_at')
    else:
        fixed_notice_list = Notice.objects.all().filter(is_fixed=True)
        notice_list = Notice.objects.all().order_by('-created_at')

    page = request.GET.get("page")
    paginator = get_paginator(notice_list, page, 10, 5)
    
    context = {
        'notice_list': notice_list,
        'fixed_notice_list': fixed_notice_list,
        "paginator": paginator,
    }
    return render(request, "board/notice_list.html", context=context)


# 공지사항 게시글 상세 페이지
def notice_detail(request, pk):




    context = {

    }
    return render(request, "board/notice_detail.html", context=context)
    

# 콘텐츠 리스트 페이지
def user_story_list(request):
    user_story_list = User_story.objects.all().order_by('-created_at')
    return render(request, "board/user_story_list.html", context={'user_story_list': user_story_list})    


# 콘텐츠 게시글 상세 페이지
def user_story_detail(request, pk):
    user_story = get_object_or_404(User_story, id=pk)

    # 조회수 증가
    user_story.hits += 1
    user_story.save()

    if request.user.is_active:
        # 로그인한 경우 좋아요 체크 유무 알려주기
        is_like = user_story.likes.filter(id=request.user.id).exists()
        return render(request, "board/user_story_detail.html", context={'user_story': user_story, 'is_like': is_like})
    else:
        return render(request, "board/user_story_detail.html", context={'user_story': user_story})    


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

    return render(request, "board/user_story_form.html", context={'form': form})


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
