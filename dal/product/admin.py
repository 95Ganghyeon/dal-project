from django.contrib import admin
from product.models import *


# Review 모델 Admin에 등록

admin.site.register(RankingBoard)
admin.site.register(Hashtag)



class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'image', 'best_review', 'score', 'price', 'count','hashtag', 'nature_friendly')

admin.site.register(Product, ProductAdmin)


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id','image','user','product','title','content','star','absorbency','anti_odour','comfort','sensitivity')

admin.site.register(Review, ReviewAdmin)

class ReviewSummaryAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'absorbency_avg', 'anti_odour_avg', 'comfort_avg', 'sensitivity_avg')

admin.site.register(ReviewSummary, ReviewSummaryAdmin)