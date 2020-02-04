from django.urls import path
from ranking import views

urlpatterns = [
    path("", views.ranking, name="ranking"),
]
