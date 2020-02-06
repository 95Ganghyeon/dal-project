from django.contrib import admin
from product.models import *
from import_export.admin import ImportExportModelAdmin

# Review 모델 Admin에 등록
admin.site.register(Hashtag)



class ProductAdmin(ImportExportModelAdmin):
    list_display = ('id', 'name', 'image', 'best_review_fk', 'price', 'count','hashtag_fk', 'nature_friendly')

admin.site.register(Product, ProductAdmin)


class ReviewAdmin(ImportExportModelAdmin):
    list_display = ('id','image','user_fk','product_fk','content','score','absorbency','anti_odour','sensitivity', 'comfort')

admin.site.register(Review, ReviewAdmin)

class ReviewSummaryAdmin(ImportExportModelAdmin):
    list_display = ('id', 'total_score','product_fk', 'absorbency_avg', 'anti_odour_avg', 'comfort_avg', 'sensitivity_avg')

admin.site.register(ReviewSummary, ReviewSummaryAdmin)