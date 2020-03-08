from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect


def user_survey_exist(function):
    def wrap(request, *args, **kwargs):
        if request.user.profile.survey_fk is None:
            return redirect('product:CompareSearch')
            # 이 부분을 survey modal 로 리다이렉트 시키는 버튼으로 연결해야 함
        else:
            return function(request, *args, **kwargs)
    
    return wrap



