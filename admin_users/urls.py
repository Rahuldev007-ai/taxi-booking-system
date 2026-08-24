from django.urls import path
from .views import (
    admin_users,
    admin_create_user,
    admin_edit_user,
    admin_delete_user,
    admin_user_detail,
    )

urlpatterns = [
    path('users/', admin_users, name='admin_users'),
    path('users/create/', admin_create_user, name='admin_create_user'),
    path('users/<int:user_id>/', admin_user_detail, name='admin_user_detail'),
    path('users/<int:user_id>/edit/', admin_edit_user, name='admin_edit_user'),
    path('users/<int:user_id>/delete/', admin_delete_user, name='admin_delete_user')    

    ]


