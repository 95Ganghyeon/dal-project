from django.shortcuts import render
from survey.forms import GetSurveyResponseForm
from survey.models import Survey

# Create your views here.
def index(request):
    if request.method == 'POST':
        get_form = GetSurveyResponseForm(request.POST)
        
        # 각 항목 계산
        if get_form.is_valid():
            q1 = int(get_form.cleaned_data['activity_score'])
            q2 = int(get_form.cleaned_data['volume_choice'])
            q3 = int(get_form.cleaned_data['volume_score'])
            q4 = len(get_form.cleaned_data.get('sensitivity_score', ''))
            q5 = len(get_form.cleaned_data.get('disease_score', ''))
            q6 = len(get_form.cleaned_data.get('volume_extra_score', ''))
            survey_result = Survey.objects.create(volume_score=q3, volume_choice=q2, sensitivity_score=q4, activity_score=q1, disease_score=q5, volume_extra_score=q6)
            
            context = {
                'mtype': survey_result.mtype
            }
            return render(request, 'index.html', context)
            
    form = GetSurveyResponseForm()
    context = {
        'form': form,
    }
    return render(request, 'index.html', context)