from django.contrib import admin

from .models import Guest, Location, Reservation

from import_export import resources
from import_export.admin import ImportExportMixin

class GuestResource(resources.Resource):
    
    # def get_display_name(self, field, instance):
    #     if field.attribute == 'guest_name':
    #         return 'My Custom Guest Name'
    #     return super().get_display_name(field, instance)

    class Meta:
        model = Guest
        fields = '__all__'

class LocationResource(resources.Resource):  

    class Meta:
        model = Location
        fields = '__all__'

class ReservationResource(resources.Resource):
    class Meta:
        model = Reservation

class GuestAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ['guest_name', 'city', 'mobile_no']
    search_fields = ['guest_name', 'city', 'mobile_no']
    resource_class = GuestResource

class LocationAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ['description', 'address', 'awas_incharge']
    search_fields = ['description', 'address', 'awas_incharge']
    resource_class = ReservationResource

admin.site.register(Guest, GuestAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Reservation)