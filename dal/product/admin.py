from django.contrib import admin
from product.models import *


# Review 모델 Admin에 등록

admin.site.register(RankingBoard)
admin.site.register(Hastag)


class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "image", "best_review")


admin.site.register(Product, ProductAdmin)


class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "id",
        "image",
        "user_id",
        "product_id",
        "content",
        "star",
        "absorbency",
        "anti_odour",
        "comfort",
        "sensitivity",
    )


admin.site.register(Review, ReviewAdmin)
