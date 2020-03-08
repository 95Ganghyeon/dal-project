from django import forms
from django.core.exceptions import ValidationError


class GetSurveyResponseForm(forms.Form):
    # 활동량
    ACTIVITY_SCORE = [
        ('6', '월경 때도 포기할 수 없는 격한 액티비티 매니아'),
        ('5', '꾸준한 운동은 나의 활력소! 월경 할 때도 운동은 필수'),
        ('4', '바깥활동은 많지만 운동은 월경 때는 가끔 가벼운 유산소 정도로'),
        ('3', '생활활동은 보통, 운동은 거의 안 해요'),
        ('2', '많이 앉아있어야 하는 직업이나 활동패턴'),
        ('1', '질문'),
    ]
    
    # 월경용품
    VOLUME_CHOICE = [
        ('1', '생리대'),
        ('2', '탐폰'),
        ('3', '생리컵'),
    ]
    
    # 월경량
    VOLUME_SCORE = [
        ('5', '3시간 내'),
        ('4', '3-4시간'),
        ('3', '4-5시간'),
        ('2', '5-6시간'),
        ('1', '6시간'),
    ]
    
    # 월경량(추가질문)
    VOLUME_EXTRA_SCORE = [
        ('0', '월경 때도 포기할 수 없는 격한 액티비티 매니아'),
        ('1', '꾸준한 운동은 나의 활력소! 월경 할 때도 운동은 필수'),
        ('2', '질문'),
        ('3', '질문'),
        ('4', '질문'),
        ('5', '질문'),
    ]
    
    # 민감도
    SENSITIVITY_SCORE = [
        ('0', '월경 때도 포기할 수 없는 격한 액티비티 매니아'),
        ('1', '꾸준한 운동은 나의 활력소! 월경 할 때도 운동은 필수'),
        ('2', '질문'),
        ('3', '질문'),
        ('4', '질문'),
        ('5', '질문'),
        ('6', '질문'),
    ]
    
    # 월경질환
    DISEASE_SCORE = [
        ('0', '월경 때도 포기할 수 없는 격한 액티비티 매니아'),
        ('1', '꾸준한 운동은 나의 활력소! 월경 할 때도 운동은 필수'),
        ('2', '질문'),
        ('3', '질문'),
        ('4', '질문'),
    ]
    
    # ---------------------------------------
    # 라디오버튼
    # ----------------------------------------
    activity_score = forms.ChoiceField(
        choices=ACTIVITY_SCORE,
        widget=forms.RadioSelect,
        label="활동량",
        required=True
    )
        
    volume_choice = forms.ChoiceField(
        choices=VOLUME_CHOICE,
        widget=forms.RadioSelect,
        label="월경용품",
        required=True
    )
    
    volume_score = forms.ChoiceField(
        choices=VOLUME_SCORE,
        widget=forms.RadioSelect,
        label="월경량",
        required=True
    )
    
    # 체크박스
    volume_extra_score = forms.MultipleChoiceField(
        choices=VOLUME_EXTRA_SCORE,
        widget=forms.CheckboxSelectMultiple,
        label="월경량(추가질문)",
        required=False
    )
    
    sensitivity_score = forms.MultipleChoiceField(
        choices=SENSITIVITY_SCORE,
        widget=forms.CheckboxSelectMultiple,
        label="민감도",
        required=False
    )
    
    disease_score = forms.MultipleChoiceField(
        choices=DISEASE_SCORE,
        widget=forms.CheckboxSelectMultiple,
        label="월경질환",
        required=False
    )