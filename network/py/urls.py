from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    url(r'likepost/$', views.like_post, name='like-post'),
    path("<str:post_id>/delete", views.delete, name="delete"),
    path("profile/<str:username>", views.profile, name="profile"),
    path("profile/<str:username>/newpost", views.newpost, name="newpost"),
    path("following/<str:username>", views.following, name='following'),
    path("posts/<int:post_id>/edit", views.edit, name="edit")
]