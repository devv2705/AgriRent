from django.urls import path
from . import views

urlpatterns = [
    path('signin/', views.signin),
    path('signup/', views.signup),
    path('verify_otp/', views.verify_otp),
    path('forgotpass/', views.pass_forgot_otp),
    path('forgot_password/', views.forgot_password),
]
