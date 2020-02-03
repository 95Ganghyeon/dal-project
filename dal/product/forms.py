from django import forms
from django.core.exceptions import ValidationError


class GetReviewResponseForm(forms.Form):
    # 종합평가
    STAR_SCORE = [
        ('1', '최악'),
        ('2', '별로'),
        ('3', '나름'),
        ('4', '오오'),
        ('5', '대박'),
    ]

    # 흡수력
    ABSORBENCY_SCORE = [
        ('1'),
        ('2'),
        ('3'),
        ('4'),
        ('5'),
    ]

    # 탈취성
    ANTI_ODOUR_SCORE = [
        ('1'),
        ('2'),
        ('3'),
        ('4'),
        ('5'),
    ]

    # 피부친화도
    SENSITIVITY_SCORE = [
        ('1'),
        ('2'),
        ('3'),
        ('4'),
        ('5'),
    ]

    # 촉감/착용감
    COMFORT_SCORE = [
        ('1'),
        ('2'),
        ('3'),
        ('4'),
        ('5'),
    ]



    # 자유의견 
    content = forms.CharField(
        widget=forms.TextInput
    )



    star_score = forms.ChoiceField(
        choices=STAR_SCORE,
        widget=forms.RadioSelect,
        label="종합평가",
        required=True
    )

    absorbency_score = forms.ChoiceField(
        choices=ABSORBENCY_SCORE,
        widget=forms.RadioSelect,
        label="흡수력",
        required=True
    )

    anti_odour_score = forms.ChoiceField(
        choices=ANTI_ODOUR_SCORE,
        widget=forms.RadioSelect,
        label="탈취성",
        required=True
    )

    sensitivity_score = forms.ChoiceField(
        choices=SENSITIVITY_SCORE,
        widget=forms.RadioSelect,
        label="피부친화도",
        required=True
    )

    comfort_score = forms.ChoiceField(
        choices=COMFORT_SCORE,
        widget=forms.RadioSelect,
        label="촉감/착용감",
        required=True
    )