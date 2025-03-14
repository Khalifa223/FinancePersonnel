from django.urls import path
from django.contrib.auth.views import (
    PasswordResetView, PasswordResetDoneView,
    PasswordResetConfirmView, PasswordResetCompleteView
)
from account import views


urlpatterns = [
    path("", views.index, name="home"),
    path("login/", views.loginView, name="login"),
    path("register/", views.register, name="register"),
    path('change-password/', views.change_password, name='change_password'),
    path('reset-password/', PasswordResetView.as_view(template_name='account/reset_password.html'), name='password_reset'),
    path('reset-password/done/', PasswordResetDoneView.as_view(template_name='account/reset_password_done.html'), name='password_reset_done'),
    path('reset-password-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='account/reset_password_confirm.html'), name='password_reset_confirm'),
    path('reset-password-complete/', PasswordResetCompleteView.as_view(template_name='account/reset_password_complete.html'), name='password_reset_complete'),
    path("logout/", views.log_out, name="logout")
]
