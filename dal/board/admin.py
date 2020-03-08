from django.contrib import admin
from board.models import *
from import_export.admin import ImportExportModelAdmin

# Register your models here.
@admin.register(Notice)
class Notice_admin(ImportExportModelAdmin):
    list_display = ('id', 'category', 'title', 'is_fixed', 'created_at')

@admin.register(User_story_origin)
class User_story_origin_admin(ImportExportModelAdmin):
    list_display = ('id', 'sort', 'user', 'title', 'created_at')

@admin.register(User_story)
class User_story_admin(ImportExportModelAdmin):
    list_display = ('id', 'user_story_origin', 'mtype', 'title', 'hits', 'total_likes', 'created_at')