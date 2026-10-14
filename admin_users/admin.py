from django.contrib import admin
from .models import User, Driver, Taxi, TaxiDetails

# Register your models here.
admin.site.register(User)
admin.site.register(Driver)

@admin.register(Taxi)
class TaxiAdmin(admin.ModelAdmin):
    list_display = ('number', 'type', 'source', 'destination', 'price', 'driver', 'get_driver_email', 'get_taxi_status')
    list_filter = ('type', 'availability')
    search_fields = ('number', 'source', 'destination', 'driver__name', 'driver__email', 'driver__license_number')

    def get_driver_email(self, obj):
        return obj.driver.email if obj.driver else "-"
    get_driver_email.short_description = 'Driver Email'

    def get_taxi_status(self, obj):
        return "Available" if obj.availability else "Unavailable"
    get_taxi_status.short_description = 'Taxi Status'

@admin.register(TaxiDetails)
class TaxiDetailsAdmin(admin.ModelAdmin):
    list_display = ('source', 'destination', 'driver_details', 'get_driver_email', 'created_at')
    search_fields = ('source', 'destination', 'driver_details__name', 'driver_details__email', 'driver_details__taxi_number')

    def get_driver_email(self, obj):
        return obj.driver_details.email if obj.driver_details else "-"
    get_driver_email.short_description = 'Driver Email'



