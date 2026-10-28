from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone

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
    """Task 54: Model named Driver with basic details, status, and taxi_number."""
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
    taxi_number = models.CharField(max_length=50, blank=True, null=True)
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


class Taxi(models.Model):
    TYPE_CHOICES = [
        ('SEDAN', 'Sedan'),
        ('SUV', 'SUV'),
        ('HATCHBACK', 'Hatchback'),
        ('PREMIUM', 'Premium'),
    ]

    number = models.CharField(max_length=50, unique=True)
    type = models.CharField(max_length=50, choices=TYPE_CHOICES, default='SEDAN')
    source = models.CharField(max_length=255)
    destination = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    availability = models.BooleanField(default=True)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, related_name='taxis')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'custom_taxis'
        verbose_name = 'Taxi'
        verbose_name_plural = 'Taxis'

    def __str__(self):
        return f"Taxi {self.number} ({self.type}) - {self.source} to {self.destination}"


class TaxiDetails(models.Model):
    """Task 54: Model named TaxiDetails along with columns: source, destination, and driver_details (FK)."""
    source = models.CharField(max_length=255)
    destination = models.CharField(max_length=255)
    driver_details = models.ForeignKey(Driver, on_delete=models.CASCADE, related_name='taxi_details')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'custom_taxi_details'
        verbose_name = 'Taxi Detail'
        verbose_name_plural = 'Taxi Details'

    def __str__(self):
        return f"{self.source} to {self.destination} (Driver: {self.driver_details.name if self.driver_details else 'None'})"


TaxiDetail = TaxiDetails


class Booking(models.Model):
    """Task 54: Model named Booking with fields: user, taxi, date, status (Pending)."""
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    taxi = models.ForeignKey(Taxi, on_delete=models.CASCADE, related_name='bookings')
    date = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'custom_bookings'
        verbose_name = 'Booking'
        verbose_name_plural = 'Bookings'
        ordering = ['-created_at']

    def __str__(self):
        return f"Booking #{self.id} - {self.user.name} for Taxi {self.taxi.number} ({self.status})"
