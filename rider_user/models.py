from django.db import models
from admin_users.models import User, Driver, Taxi, TaxiDetails, TaxiDetail, Booking

# Task 54: Models for Taxi Details, Driver, and Booking accessible to rider_user app
__all__ = ['User', 'Driver', 'Taxi', 'TaxiDetails', 'TaxiDetail', 'Booking']
