from django.contrib import admin
from product.models import *
from import_export.admin import ImportExportModelAdmin

# Review 모델 Admin에 등록

admin.site.register(Hashtag)



class ProductAdmin(ImportExportModelAdmin):
    list_display = ('id', 'name', 'image', 'best_review_fk', 'price', 'count')
admin.site.register(Product, ProductAdmin)

class ProductIngredientAdmin(ImportExportModelAdmin):
    list_display = ('id', 'product_fk','cover_layer_score','absorbent_layer_score','etc_score','cover_layer_string','absorbent_layer_string','etc_string','nature_friendly_score')
admin.site.register(ProductIngredient, ProductIngredientAdmin)

class ReviewAdmin(ImportExportModelAdmin):
    list_display = ('id','image','user_fk','m_type','product_fk','content','score','absorbency','anti_odour','sensitivity', 'comfort')
admin.site.register(Review, ReviewAdmin)
