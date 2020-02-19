from django.urls import path
from product import views

app_name = 'product'
urlpatterns = [
    path('<int:pk>/', views.productDetail, name="ProductDetail"),
    path('normalsearch/', views.normalSearch, name='NormalSearch'),    
    path('comparesearch/', views.compareSearch, name='CompareSearch'),
    path('cart/insert/<int:product_id>/', views.insert_cart, name='insert-cart'),
    path('cart/delete/<int:product_id>/', views.delete_cart, name='delete-cart'),
]
