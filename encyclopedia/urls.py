from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.get_page, name="TITLE"),
    path("search", views.search, name="search"),
]
