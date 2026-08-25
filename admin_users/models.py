from django.db import models
from django.contrib.auth.hashers import make_password, check_password
    
# Create your models here.

class User(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField(max_length=254, unique=True)
    mobile = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta: 
        db_table = 'custom_users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return f"{self.name} ({self.email})"
    
class Driver(models.Model):
    STATUS_CHOICES = [
            ('AVAILABLE', 'Available'),
            ('ON_TRIP', 'On Trip'),
            ('OFFLINE', 'Offline'),
        ]
    name = models.CharField(max_length=150)
    email = models.EmailField(max_length=254, unique=True)
    license_number = models.CharField(max_length=50, unique=True)
    mobile = models.CharField(max_length=20, unique=True)
    vehicle_name = models.CharField(max_length=100, blank=True, null=True, default="Toyota Camry Hybrid")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='AVAILABLE')    
    password = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'custom_drivers'
        verbose_name = 'Driver'
        verbose_name_plural = 'Drivers'

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return f"{self.name} (License: {self.license_number})"