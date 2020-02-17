from django.contrib import admin
from ranking.models import *
from import_export.admin import ImportExportModelAdmin


# Register your models here.


class RankingBoardAdmin(ImportExportModelAdmin):
    list_display = ('product_fk', 'm_type', 'score_avg')
admin.site.register(RankingBoard, RankingBoardAdmin)

class ReviewSummaryAdmin(ImportExportModelAdmin):
    list_display = ('id', 'product_fk', 'total_score', 'absorbency_avg', 'anti_odour_avg', 'comfort_avg', 'sensitivity_avg')
admin.site.register(ReviewSummary, ReviewSummaryAdmin)

