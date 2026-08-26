from django.urls import path
from .views import (user_register)

urlpatterns = [
    path('user/register/',user_register,name="user-register" ),
]
