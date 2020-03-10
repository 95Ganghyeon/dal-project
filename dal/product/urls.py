from django.urls import path
from product import views

app_name = 'product'
urlpatterns = [
    path('<int:pk>/', views.productDetail, name="ProductDetail"),
    path('normalsearch/', views.normalSearch, name='NormalSearch'),    
    path('comparesearch/', views.compareSearch, name='CompareSearch'),
    path('cart/<int:product_id>/', views.cart, name='cart'),
    path('<int:pk>/addmyproduct', views.add_myProduct, name='add_myProduct'),
    path('<int:pk>/addzzimproduct', views.add_zzimProduct, name='add_zzimProduct'),
]
