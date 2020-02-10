from django.contrib import admin
from ranking.models import RankingBoard
from import_export.admin import ImportExportModelAdmin


# Register your models here.


class RankingBoardAdmin(ImportExportModelAdmin):
    list_display = ('product_fk', 'm_type', 'score_avg')

admin.site.register(RankingBoard, RankingBoardAdmin)

