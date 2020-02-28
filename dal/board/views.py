from django.shortcuts import render

def notice_detail(request, pk):
    return render(request, "notice_detail.html", context={})

def user_story_detail(request, pk):
    return render(request, "user_story_detail.html", context={})
