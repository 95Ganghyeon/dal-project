from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from product.views import get_paginator
from user.models import *
from .models import *
from .forms import UserStroyForm
from django.db.models import (
    Case, When, Value, BooleanField, Exists,
    F, Func, Value, Q
)

def get_paginator(obj, page, obj_per_page, page_range):
    page = int(page) if page else 1

    paginator = Paginator(obj, obj_per_page)
    max_page = paginator.num_pages  # 마지막 페이지
    start_page = int((page - 1) / page_range) * page_range
    end_page = start_page + page_range
    if end_page >= max_page:
        end_page = max_page

    return {
        "page_obj": paginator.get_page(page),
        "page_range": paginator.page_range[start_page:end_page],
        "has_prev": True if start_page > 1 else False,
        "has_next": True if end_page < max_page else False,
        "prev_page": (start_page),
        "next_page": (end_page + 1),
    }


# 공지사항 리스트 페이지
def notice_list(request):
    
    def makeNoticeList(**kwargs):
        # 카테코리 탭을 누른 경우
        if 'category' in kwargs.keys():
            if kwargs['category'] == "entire":
                fixed_notice_list = Notice.objects.all().filter(is_fixed=True).order_by('-created_at')
                notice_list = Notice.objects.all().order_by('-created_at')
            elif kwargs['category'] == "notice":
                fixed_notice_list = Notice.objects.all().filter(category="notice", is_fixed=True).order_by('-created_at')
                notice_list = Notice.objects.all().filter(category="notice").order_by('-created_at')
            elif kwargs['category'] == "event":
                fixed_notice_list = Notice.objects.all().filter(category="event", is_fixed=True).order_by('-created_at')
                notice_list = Notice.objects.all().filter(category="event").order_by('-created_at')
        # 검색어를 입력한 경우
        if 'query' in kwargs.keys():
            fixed_notice_list = Notice.objects.all().filter(is_fixed=True).order_by('-created_at')
            query = kwargs['query']
            notice_list = Notice.objects.all().annotate(
            rename1=Func(
                F("title"), Value(" "), Value(""), function="REPLACE"
            ),
            rename2=Func(
                F("content"), Value(" "), Value(""), function="REPLACE"
            )
            ).filter(Q(rename1__icontains=query)|Q(rename2__icontains=query))
        # 최초에 페이지를 랜더링할 경우(디폴트)
        if 'default' in kwargs.keys():
            fixed_notice_list = Notice.objects.all().filter(is_fixed=True).order_by('-created_at')
            notice_list = Notice.objects.all().order_by('-created_at')
        
        return fixed_notice_list, notice_list
        
        
    # 쿼리스트링 생성 for paginator
    query_string = ""
    if request.META["QUERY_STRING"]:
        for item in request.META["QUERY_STRING"].split("&"):
            if "page" not in item:
                query_string += "&" + item

    # notice_list 생성
    if request.GET.get("category"):
        fixed_notice_list, notice_list = makeNoticeList(category=request.GET.get("category"))
    elif request.GET.get("q"):
        fixed_notice_list, notice_list = makeNoticeList(query=request.GET.get("q").replace(" ", ""))
    else:
        fixed_notice_list, notice_list = makeNoticeList(default="")
    
    page = request.GET.get("page")
    paginator = get_paginator(notice_list, page, 10, 5)
    context = {
        'notice_list': notice_list,
        'fixed_notice_list': fixed_notice_list,
        "paginator": paginator,
        'query_string': query_string,
    }
    return render(request, "board/notice_list.html", context=context)


# 공지사항 게시글 상세 페이지
def notice_detail(request, pk):
    notice = get_object_or_404(Notice, id=pk)
    
    # 조회수 증가
    notice.hits += 1
    notice.save()

    # 이전글/다음글
    prev_notice = Notice.objects.filter(created_at__lt=notice.created_at).order_by('-created_at').first()
    next_notice = Notice.objects.filter(created_at__gt=notice.created_at).order_by('created_at').first()
    

    context = {
        'notice': notice,
        'prev_notice': prev_notice,
        'next_notice': next_notice,
    }
    return render(request, "board/notice_detail.html", context=context)
    

# 콘텐츠 리스트 페이지
def user_story_list(request):
    user_story_list = None
    query_string = ''
    option = ''

    if 'option' in request.GET:
        option = request.GET.get('option')
        if option == 'created_at':
            user_story_list = User_story.objects.all().order_by('-created_at')
        else:
            user_story_list = sorted(User_story.objects.all(), key=lambda t: t.total_likes, reverse=True)
    else:
        user_story_list = User_story.objects.all().order_by('-created_at')


    # 쿼리스트링 생성 for paginator
    if request.META["QUERY_STRING"]:
        for item in request.META["QUERY_STRING"].split("&"):
            if "page" not in item:
                query_string += "&" + item


    page = request.GET.get("page")
    paginator = get_paginator(user_story_list, page, 3, 2)

    context = {
        'user_story_list': user_story_list,
        'paginator': paginator,
        'query_string': query_string,
    }

    return render(request, "board/user_story_list.html", context=context)    


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
