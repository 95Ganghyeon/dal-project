from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from allauth.socialaccount.models import SocialAccount
from .models import *
from import_export.admin import ImportExportModelAdmin

# Register your models here.
class UserAdmin(ImportExportModelAdmin):
  pass

#overide default user admin 
admin.site.unregister(User)
@admin.register(User)
class CustomUserAdmin(UserAdmin):
  list_per_page = 5
  list_display = ('id','username','email','is_active','return_social')
  #clickable
  list_display_links = ('id','username','email')
  #list_editable = ('permission')
  list_filter = ('is_active',)
  search_fields = ('username','email',)
  ordering = ('-id','username','email',)

  fieldsets = (
    (None, {'fields':('username','email','password')}),
    #('프로필', {'fields':('')}),

  )
  def return_social(self,obj):
    try:
      return SocialAccount.objects.get(user=obj).provider
    except:
      return 'none'


class ProfileAdmin(ImportExportModelAdmin):
  list_display = ('id', 'user_fk', 'ghost_user', 'm_type', 'survey_fk', 'age')

admin.site.register(Profile, ProfileAdmin)

