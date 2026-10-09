from django.urls import path
from .views import (
    user_register, 
    user_login, 
    driver_login,
    driver_logout,
    user_dashboard, 
    driver_dashboard,
    driver_profile,
    user_logout, 
    driver_register,
    driver_verify_otp,
    driver_resend_otp,
    user_forgot_password,
    user_verify_otp,
    user_reset_password
)

urlpatterns = [
    path('user/register/', user_register, name="user-register"),
    path('driver/register/', driver_register, name="driver-register"),
    path('driver-register/', driver_register, name="driver_register"),
    path('driver/verify-otp/', driver_verify_otp, name="driver-verify-otp"),
    path('driver-verify-otp/', driver_verify_otp, name="driver_verify_otp"),
    path('driver/resend-otp/', driver_resend_otp, name="driver-resend-otp"),
    path('driver/login/', driver_login, name="driver-login"),
    path('driver-login/', driver_login, name="driver_login"),
    path('driver/logout/', driver_logout, name="driver-logout"),
    path('driver-logout/', driver_logout, name="driver_logout"),
    path("user/dashboard", user_dashboard, name="user-dashboard"),
    path("driver/dashboard/", driver_dashboard, name="driver-dashboard"),
    path("driver/dashboard", driver_dashboard, name="driver-dashboard-alt"),
    path("driver/profile/", driver_profile, name="driver-profile"),
    path("driver/profile", driver_profile, name="driver-profile-alt"),
    path('user/login/', user_login, name="user_login"),
    path('user/logout/', user_logout, name="user_logout"),
    path('user/forgot-password/', user_forgot_password, name="user_forgot_password"),
    path('user/verify-otp/', user_verify_otp, name="user_verify_otp"),
    path('user/reset-password/', user_reset_password, name="user_reset_password"),
]

