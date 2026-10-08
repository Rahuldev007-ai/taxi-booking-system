from django.urls import path
from .views import (
    user_register, 
    user_login, 
    user_dashboard, 
    user_logout, 
    driver_register,
    user_forgot_password,
    user_verify_otp,
    user_reset_password
)

urlpatterns = [
    path('user/register/', user_register, name="user-register"),
    path('driver/register/', driver_register, name="driver-register"),
    path('driver-register/', driver_register, name="driver_register"),
    path("user/dashboard", user_dashboard, name="user-dashboard"),
    path('user/login/', user_login, name="user_login"),
    path('user/logout/', user_logout, name="user_logout"),
    path('user/forgot-password/', user_forgot_password, name="user_forgot_password"),
    path('user/verify-otp/', user_verify_otp, name="user_verify_otp"),
    path('user/reset-password/', user_reset_password, name="user_reset_password"),
]
