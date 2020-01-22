from django.contrib import admin
from survey.models import Survey

# Register your models here.

@admin.register(Survey)
class SurveyAdmin(admin.ModelAdmin):
    pass