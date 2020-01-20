from django.contrib import admin
from product.models import *


# Review 모델 Admin에 등록
admin.site.register(Review)
admin.site.register(RankingBoard)
admin.site.register(Hastag)


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'image')

admin.site.register(Product, ProductAdmin)

