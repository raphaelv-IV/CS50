from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("categories", views.categories, name="categories"),
    path("category/<str:prod_cat>", views.category, name="category"),
    path("active_listing", views.active_listing, name="active_listing"),
    path("view_listing/<int:prod_id>", views.view_listing, name="view_listing"),
    path("add_watchlist/<int:prod_id>", views.add_watchlist, name="add_watchlist"),
    path("add_comment/<int:prod_id>", views.add_comment, name="add_comment"),
    path("close_bid/<int:prod_id>", views.close_bid, name="close_bid"),
    path("watch_list", views.watch_list, name="watch_list")
]

