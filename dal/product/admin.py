from django.contrib import admin
from product.models import *


# Review 모델 Admin에 등록
admin.site.register(Hashtag)



class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'image', 'best_review_fk', 'price', 'count','hashtag_fk', 'nature_friendly')

admin.site.register(Product, ProductAdmin)


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id','image','user_fk','product_fk','content', 'absorbency','anti_odour','sensitivity', 'comfort', 'score')

admin.site.register(Review, ReviewAdmin)

class ReviewSummaryAdmin(admin.ModelAdmin):
    list_display = ('id', 'product_fk', 'absorbency_avg', 'anti_odour_avg', 'comfort_avg', 'sensitivity_avg')

admin.site.register(ReviewSummary, ReviewSummaryAdmin)