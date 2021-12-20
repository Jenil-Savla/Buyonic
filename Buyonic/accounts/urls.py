from django.urls import path 
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/',views.RegisterAPI.as_view(),name="register"),
    path('login/',views.LoginAPI.as_view(),name="login"),
    path('otp/',views.OTPView.as_view(),name="otp"),
    path('logout/',views.LogoutAPI.as_view(),name="logout"),
    path('email-verify/',views.EmailVerify.as_view(),name="email-verify"),
    path('waiting/',views.Waiting.as_view(),name="waiting"),
    path('profile/',views.Profile.as_view(),name="profile"),

    path('password_reset',auth_views.PasswordResetView.as_view(),name='password-reset'),
    path('password_reset/done',auth_views.PasswordResetDoneView.as_view(),name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>',auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    path('reset/done',auth_views.PasswordResetCompleteView.as_view(),name='password_reset_complete'),
]