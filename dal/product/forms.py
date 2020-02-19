from django import forms
from django.core.exceptions import ValidationError
from .models import Review


class GetReviewResponseForm(forms.Form):

    SCORE = (
        ("5", "5"),
        ("4", "4"),
        ("3", "3"),
        ("2", "2"),
        ("1", "1"),
    )

    ABSORBENCY = (
        ("5", "아주 만족스러웠고"),
        ("4", "꽤 괜찮았고"),
        ("3", "무난했고"),
        ("2", "축축함이 느껴질 정도였고"),
        ("1", "최악이었고"),
    )

    ANTI_ODOUR = (
        ("5", "아주 깔끔하게 잡아줬다"),
        ("4", "꽤 잘 잡아줬다"),
        ("3", "그럭저럭 잡아줬다"),
        ("2", "거의 잡아주지 못했다"),
        ("1", "전혀 잡아주지 못했다"),
    )

    SENSITIVITY = (
        ("5", "최고로 좋았고"),
        ("4", "꽤 괜찮았고"),
        ("3", "무난했고"),
        ("2", "살짝 불편했고"),
        ("1", "최악이었고"),
    )

    COMFORT = (
        ("5", "전혀 자극이 없었다"),
        ("4", "꽤 순한 느낌이었다"),
        ("3", "무난했다"),
        ("2", "자극이 느껴질 정도로 불편했다"),
        ("1", "최악이었다"),
    )

    score = forms.ChoiceField(choices=SCORE)
    absorbency = forms.ChoiceField(choices=ABSORBENCY)
    anti_odour = forms.ChoiceField(choices=ANTI_ODOUR)
    sensitivity = forms.ChoiceField(choices=SENSITIVITY)
    comfort = forms.ChoiceField(choices=COMFORT)
    content = forms.CharField(
        max_length=1000,
        widget=forms.Textarea(
            attrs={"cols": 60, "rows": 15, "class": "textarea w-100 mb-3"}
        ),
    )

    # class Meta:
    #     model = Review
    #     fields = [
    #         "score",
    #         "absorbency",
    #         "anti_odour",
    #         "sensitivity",
    #         "comfort",
    #         "content",
    #     ]
    #     widgets = {
    #         "score": forms.RadioSelect,
    #         "absorbency": forms.RadioSelect,
    #         "anti_odour": forms.RadioSelect,
    #         "sensitivity": forms.RadioSelect,
    #         "comfort": forms.RadioSelect,
    #     }


# star_score = forms.ChoiceField(
#     choices=,
#     widget=forms.RadioSelect,
#     label="종합평가",
#     required=True
# )

# absorbency_score = forms.ChoiceField(
#     choices=ABSORBENCY_SCORE,
#     widget=forms.RadioSelect,
#     label="흡수력",
#     required=True
# )

# anti_odour_score = forms.ChoiceField(
#     choices=ANTI_ODOUR_SCORE,
#     widget=forms.RadioSelect,
#     label="탈취성",
#     required=True
# )

# sensitivity_score = forms.ChoiceField(
#     choices=SENSITIVITY_SCORE,
#     widget=forms.RadioSelect,
#     label="피부친화도",
#     required=True
# )

# comfort_score = forms.ChoiceField(
#     choices=COMFORT_SCORE,
#     widget=forms.RadioSelect,
#     label="촉감/착용감",
#     required=True
# )

# content = forms.CharField(
#     widget=forms.TextInput
# )


"""
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
"""
