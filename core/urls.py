from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import admin_login

urlpatterns = [
    path('', admin_login, name='admin_login_root'),
    path('login/', admin_login, name='admin_login_alt'),
    path('AdminLogin/', admin_login, name='admin_login'),
]

