
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("home/<str:criteria>", views.home, name="home"),
    path("create", views.create, name="create"),
    path("view/<int:entry_number>", views.view, name="view"),
    path("copy/<int:entry_number>", views.copy, name="copy"),
    path("update/<int:entry_number>", views.update_entry, name="update"),
    path("delete/<int:entry_number>", views.delete_entry, name="delete"),
    path("meditate", views.meditate, name="meditate"),
    path("profile", views.profile, name="profile"),
    path("emotions", views.emotions, name="emotions"),
]
