from django.urls import path
from .views import (user_register,user_login,user_dashboard,user_logout)

urlpatterns = [
    path('user/register/',user_register,name="user-register"),
    path("user/dashboard",user_dashboard, name="user-dashboard"),
    path('user/login/',user_login,name="user_login"),
    path('user/logout/',user_logout,name="user_logout"),
]
