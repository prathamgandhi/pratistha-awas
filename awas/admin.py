from django.contrib import admin
from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple

from .models import Guest, Location, Reservation

from import_export import fields, resources
from import_export.admin import ImportExportMixin
from import_export.widgets import ForeignKeyWidget


class GuestAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ['guest_name', 'city', 'mobile_no']
    search_fields = ['guest_name', 'city', 'mobile_no']
    # resource_class = GuestResource

class GuestAdminInlineForm(forms.ModelForm):
    class Meta:
        model = Guest
        fields = '__all__'
    
    existing_guest = forms.ModelMultipleChoiceField(
        queryset=Guest.objects.all(),
        label="Select guest",
        required=True,
    )

class GuestAdminInline(admin.StackedInline):
    model = Guest
    # raw_id_fields = (
    #     'reservation',
    # )
    extra = 0
    form = GuestAdminInlineForm
    fields = ['existing_guest']

class LocationAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ['description', 'address', 'awas_incharge']
    search_fields = ['description', 'address', 'awas_incharge']
    # resource_class = LocationResource

class LocationAdminInline(admin.TabularInline):
    model = Location
    extra = 0
    autocomplete_fields = ['reservation']

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = '__all__'

    guests = forms.ModelMultipleChoiceField(
        queryset=Guest.objects.all(),
        widget=FilteredSelectMultiple('Guests', is_stacked=False),
    )

    def __init__(self, *args, **kwargs):
        super(ReservationForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['guests'].initial = self.instance.guest_set.all()

    def save(self, *args, **kwargs):
        instance = super(ReservationForm, self).save(commit=False)
        instance.save()
        # Clear the association for existing guests
        print(instance)
        print(self.cleaned_data)
        print(self.fields)
        for guest in self.cleaned_data['guests']:
            guest.reservation = instance
            guest.save()

        # Update the association for the selected guests
        # self.cleaned_data['guests'].update(reservation=instance)
        return instance

class ReservationAdmin(ImportExportMixin, admin.ModelAdmin):
    # resource_class = ReservationResource
    form = ReservationForm
    raw_id_fields = ['location']

    def save_model(self, request, obj, form, change):
        print(obj)
        super().save_model(request, obj, form, change)

admin.site.register(Guest, GuestAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Reservation, ReservationAdmin)