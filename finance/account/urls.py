from django.urls import path
from account import views

urlpatterns = [
    path("", views.index, name="home"),
    path("login/", views.loginView, name="login"),
    path("register/", views.register, name="register"),
    path("logout/", views.log_out, name="logout")
]
