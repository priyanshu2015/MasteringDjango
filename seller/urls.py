from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('signup/', views.RegisterView.as_view(), name="signup"),
    path('signupseller/', views.RegisterViewSeller.as_view(), name="signupseller"),
    path('login/', views.LoginViewUser.as_view(), name="login"),
    path('logout/', views.LogoutViewUser.as_view(), name="logout"),

    #path('sendotp/', views.otp_send, name = "sendotp"),
    #path('verifyotp/', views.otp_verify, name = "verifyotp"),
]