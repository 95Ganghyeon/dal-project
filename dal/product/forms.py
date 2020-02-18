from django import forms
from django.core.exceptions import ValidationError
from .models import Review


class GetReviewResponseForm(forms.Form):

    SCORE = (
        ("1", "1"),
        ("2", "2"),
        ("3", "3"),
        ("4", "4"),
        ("5", "5"),
    )

    ABSORBENCY = (
        ("1", "최악이었다"),
        ("2", "자극이 느껴질 정도로 불편했다"),
        ("3", "무난했다"),
        ("4", "나름 순한 느낌이다"),
        ("5", "전혀 자극이 느껴지지 않고 최고였다."),
    )

    ANTI_ODOUR = (
        ("1", "최악이었다"),
        ("2", "자극이 느껴질 정도로 불편했다"),
        ("3", "무난했다"),
        ("4", "나름 순한 느낌이다"),
        ("5", "전혀 자극이 느껴지지 않고 최고였다."),
    )

    SENSITIVITY = (
        ("1", "최악이었다"),
        ("2", "자극이 느껴질 정도로 불편했다"),
        ("3", "무난했다"),
        ("4", "나름 순한 느낌이다"),
        ("5", "전혀 자극이 느껴지지 않고 최고였다."),
    )

    COMFORT = (
        ("1", "최악이었다"),
        ("2", "자극이 느껴질 정도로 불편했다"),
        ("3", "무난했다"),
        ("4", "나름 순한 느낌이다"),
        ("5", "전혀 자극이 느껴지지 않고 최고였다."),
    )

    score = forms.ChoiceField(choices=SCORE)
    absorbency = forms.ChoiceField(choices=ABSORBENCY)
    anti_odour = forms.ChoiceField(choices=ANTI_ODOUR)
    sensitivity = forms.ChoiceField(choices=SENSITIVITY)
    comfort = forms.ChoiceField(choices=COMFORT)
    content = forms.CharField(max_length=400)

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
