from django.contrib import admin
from django.shortcuts import render
from ranking.models import *
from ranking.views import updateRankingBoard, updateReviewSummary
from import_export.admin import ImportExportModelAdmin
from django.urls import path
from django.http import HttpResponseRedirect


# Register your models here.


class RankingBoardAdmin(ImportExportModelAdmin):
    list_display = ('product_fk', 'm_type', 'score_avg')
    list_filter = ('m_type', 'product_fk')
    # 업데이트 버튼 나오게 하려면 아래 부분 활성화!!
    # change_list_template = 'ranking/rankingboard_update.html'

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('update/', self.update),
        ]
        return my_urls + urls

    def update(self, request):
        updateRankingBoard()
        self.message_user(request, "Ranking Board 업데이트 완료")
        return HttpResponseRedirect("../")


class ReviewSummaryAdmin(ImportExportModelAdmin):
    list_display = ('id', 'product_fk', 'total_score', 'absorbency_avg', 'anti_odour_avg', 'comfort_avg', 'sensitivity_avg')
    # 업데이트 버튼 나오게 하려면 아래 부분 활성화!!
    # change_list_template = 'ranking/reviewsummary_update.html'


    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('update/', self.update),
        ]
        return my_urls + urls

    def update(self, request):
        updateReviewSummary()
        self.message_user(request, "Review Summary 업데이트 완료")
        return HttpResponseRedirect("../")


admin.site.register(RankingBoard, RankingBoardAdmin)
admin.site.register(ReviewSummary, ReviewSummaryAdmin)

