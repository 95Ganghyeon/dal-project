from django.contrib import admin
from survey.models import Survey
from import_export.admin import ImportExportModelAdmin

# Register your models here.
@admin.register(Survey)
class SurveyAdmin(ImportExportModelAdmin):
    list_display = ('id', 'mtype')

