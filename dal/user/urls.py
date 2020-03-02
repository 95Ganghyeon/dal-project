from django.urls import path
from user import views

urlpatterns = [
    path('profile/', views.profile, name='profile'),
    path('profile/edit', views.edit_profile, name='edit_profile'), 
    path('profile/delete/<int:product_id>', views.delete_myProduct, name='delete_myProduct'),
]