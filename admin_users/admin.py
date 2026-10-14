from django.contrib import admin
from .models import User, Driver, Taxi, TaxiDetails

# Register your models here.
admin.site.register(User)
admin.site.register(Driver)

@admin.register(Taxi)
class TaxiAdmin(admin.ModelAdmin):
    list_display = ('number', 'type', 'source', 'destination', 'price', 'availability', 'driver')
    list_filter = ('type', 'availability')
    search_fields = ('number', 'source', 'destination', 'driver__name', 'driver__license_number')

@admin.register(TaxiDetails)
class TaxiDetailsAdmin(admin.ModelAdmin):
    list_display = ('source', 'destination', 'driver_details', 'created_at')
    search_fields = ('source', 'destination', 'driver_details__name', 'driver_details__taxi_number')


