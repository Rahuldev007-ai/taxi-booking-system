from django.urls import path
from .views import (user_register, user_login, user_dashboard, user_logout, driver_register)

urlpatterns = [
    path('user/register/', user_register, name="user-register"),
    path('driver/register/', driver_register, name="driver-register"),
    path('driver-register/', driver_register, name="driver_register"),
    path("user/dashboard", user_dashboard, name="user-dashboard"),
    path('user/login/', user_login, name="user_login"),
    path('user/logout/', user_logout, name="user_logout"),
]
