from django.urls import path
from .views import admin_login, admin_register, admin_logout,admin_dashboard,admin_forgot_password

urlpatterns = [
    path('', admin_login, name='admin_login_root'),
    path('login/', admin_login, name='admin_login_alt'),
    path('AdminLogin/', admin_login, name='admin_login'),
    path('register/', admin_register, name='admin_register'),
    path('AdminRegister/', admin_register, name='admin_register_alt'),
    path('logout/', admin_logout, name='admin_logout'),
    path('dashboard/', admin_dashboard, name='admin_dashboard'),
    path('forgot-password/', admin_forgot_password, name='admin_forgot_password'),
]


