from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("edit/<str:title>", views.edit_page, name="edit_page"),
    path("create/", views.new_page, name="new_page"),
    path("wiki/<str:title>", views.entry_page, name="entry_page"),
    path("wiki/", views.random_page, name="random_page")
]