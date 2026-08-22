from django.urls import path
from .views import (
    admin_login, 
    admin_register, 
    admin_logout,
    admin_dashboard,
    admin_forgot_password,
    admin_verify_otp,
    admin_reset_password,
    admin_drivers,
    admin_users,
    admin_bookings,
    )

urlpatterns = [
    path('', admin_login, name='admin_login_root'),
    path('login/', admin_login, name='admin_login_alt'),
    path('AdminLogin/', admin_login, name='admin_login'),
    path('register/', admin_register, name='admin_register'),
    path('AdminRegister/', admin_register, name='admin_register_alt'),
    path('logout/', admin_logout, name='admin_logout'),
    path('dashboard/', admin_dashboard, name='admin_dashboard'),
    path('AdminForgotPassword/', admin_forgot_password, name='admin_forgot_password_alt'),
    path('verify-otp/', admin_verify_otp, name='admin_verify_otp'),
    path('reset-password/', admin_reset_password, name='admin_reset_password'),
    path('forgot-password/', admin_forgot_password, name='admin_forgot_password'),
    path('drivers/', admin_drivers, name='admin_drivers'),
    path('users/', admin_users, name='admin_users'),
    path('bookings/', admin_bookings, name='admin_bookings'),
]


