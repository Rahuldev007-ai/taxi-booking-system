from django.db import models
from admin_users.models import (
    User, Driver, Taxi, TaxiDetails, TaxiDetail, Booking,
    driver, taxi, taxi_details, Taxi_Details, taxi_detail, booking
)

# Task 54 & Task 60: Models for Taxi Details, Driver, and Booking accessible to rider_user app
__all__ = [
    'User', 'Driver', 'Taxi', 'TaxiDetails', 'TaxiDetail', 'Booking',
    'driver', 'taxi', 'taxi_details', 'Taxi_Details', 'taxi_detail', 'booking'
]
