from django.urls import path
from . import views

urlpatterns = [
    path('signup', views.SignupView.as_view(), name='signup'),
    path('login', views.user_login, name='login'),
    path('logout', views.user_logout, name='logout'),
    path('resend-code', views.resend_code, name='resend_code'),
    path('verify-email', views.VerifyEmailView.as_view(), name='verify_email'),
]
