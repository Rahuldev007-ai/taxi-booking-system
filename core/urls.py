from django.urls import path
from .views import admin_login, admin_register, admin_logout

urlpatterns = [
    path('', admin_login, name='admin_login_root'),
    path('login/', admin_login, name='admin_login_alt'),
    path('AdminLogin/', admin_login, name='admin_login'),
    path('register/', admin_register, name='admin_register'),
    path('AdminRegister/', admin_register, name='admin_register_alt'),
    path('logout/', admin_logout, name='admin_logout'),
]


