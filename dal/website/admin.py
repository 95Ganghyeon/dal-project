from django.contrib import admin
from website.models import Survey

# Register your models here.

@admin.register(Survey)
class BookAdmin(admin.ModelAdmin):
    pass