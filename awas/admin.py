import os 

from django.contrib import admin
from django import forms
from django.utils.html import format_html, mark_safe
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.forms.models import model_to_dict

from .models import Guest, Location, Cities, States, Districts, Countries, UserRegistration #, Reservation

from import_export import fields, resources
from import_export.admin import ImportExportMixin
from import_export.widgets import ForeignKeyWidget

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Table, TableStyle, Paragraph, Spacer, NextPageTemplate, PageBreak
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch

from django.http import HttpResponse
from django.core.files.storage import default_storage

from .utils import ReportTemplate, fill_location_wise_allotment

# class LocationAdminInline(admin.TabularInline):
#     model = Location
#     extra = 0
#     readonly_fields = (
#         'description',
#         'address',
#         'capacity',
#     )
#     def has_change_permission(self, request, obj=None):
#         return False

class GuestResource(resources.ModelResource):
    location = fields.Field(
        column_name='location',
        attribute='location',
        widget=ForeignKeyWidget(Location, 'description')
    )
    class Meta:
        model = Guest
        fields = (
            'guest_name',
            'city',
            'location',
            'mobile_no',
            'ext_reg_no',
            'no_of_persons',
        )
        export_order = (
            'guest_name',
            'city',
            'location',
            'mobile_no',
            'ext_reg_no',
            'no_of_persons',
        )

class GuestAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ['guest_name', 'city', 'mobile_no', 'arrival_date', 'departure_date']
    search_fields = ['guest_name', 'city', 'mobile_no']
    raw_id_fields = (
        'location',
    )
    # inlines = [LocationAdminInline]
    resource_class = GuestResource

class GuestAdminInline(admin.TabularInline):
    model = Guest
    extra = 0
    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False



class LocationAdmin(ImportExportMixin, admin.ModelAdmin):
    inlines = [GuestAdminInline]
    list_display = ['description', 'address', 'awas_incharge', 'capacity', 'reserved']
    search_fields = ['description', 'address', 'awas_incharge']
    readonly_fields = ('reserved',)

    actions = ["generate_location_report"]

    @admin.action(description="Generate Locationwise allotment report")
    def generate_location_report(self, request, queryset):

        story = []       
        story.append(NextPageTemplate('NormalPage'))

        fill_location_wise_allotment(queryset, story)        

        # Create pdf and send response
        filename = "location-wise-report.pdf"
        pdf_directory = "generated_pdfs/"
        os.makedirs(pdf_directory, exist_ok=True)
        pdf_file_path = os.path.join(pdf_directory, filename)
        pdf_buffer = default_storage.open(pdf_file_path, 'wb')
        pdf_document = ReportTemplate(pdf_buffer, pagesize=letter)
        pdf_document.build(story)
        pdf_buffer.close()
        pdf_buffer = default_storage.open(pdf_file_path, 'rb')
        response = HttpResponse(pdf_buffer, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="location-wise-report.pdf"'

        return response
    # resource_class = LocationResource


# class ReservationForm(forms.ModelForm):
#     class Meta:
#         model = Reservation
#         fields = '__all__'

#     guests = forms.ModelMultipleChoiceField(
#         queryset=Guest.objects.all(),
#         widget=FilteredSelectMultiple('Guests', is_stacked=False),
#     )

#     def __init__(self, *args, **kwargs):
#         super(ReservationForm, self).__init__(*args, **kwargs)
#         if self.instance and self.instance.pk:
#             self.fields['guests'].initial = self.instance.guest_set.all()

#     def save(self, *args, **kwargs):
#         instance = super(ReservationForm, self).save(commit=False)
#         instance.save()
#         # Clear the association for existing guests
#         print(instance)
#         for guest in self.cleaned_data['guests']:
#             guest.reservation = instance
#             guest.save()

#         # Update the association for the selected guests
#         # self.cleaned_data['guests'].update(reservation=instance)
#         return instance

# class ReservationAdmin(ImportExportMixin, admin.ModelAdmin):
#     # resource_class = ReservationResource
#     form = ReservationForm
#     raw_id_fields = ['location']

#     def save_model(self, request, obj, form, change):
#         print(obj)
#         super().save_model(request, obj, form, change)

class CitiesAdmin(admin.ModelAdmin):
    using = 'remote'

    def get_queryset(self, request):
        return super(CitiesAdmin, self).get_queryset(request).using(self.using)

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

class DistrictsAdmin(admin.ModelAdmin):
    using = 'remote'

    def get_queryset(self, request):
        return super(DistrictsAdmin, self).get_queryset(request).using(self.using)
    
    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

class StatesAdmin(admin.ModelAdmin):
    using = 'remote'

    def get_queryset(self, request):
        return super(StatesAdmin, self).get_queryset(request).using(self.using)

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

class CountriesAdmin(admin.ModelAdmin):
    using = 'remote'

    def get_queryset(self, request):
        return super(CountriesAdmin, self).get_queryset(request).using(self.using)

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

class UserRegistrationAdmin(admin.ModelAdmin):
    using = 'remote'

    search_fields = ['mobile']
    list_display = ['first_name', 'middle_name', 'last_name', 'mobile']

    def get_queryset(self, request):
        return super(UserRegistrationAdmin, self).get_queryset(request).using(self.using)

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

admin.site.register(Guest, GuestAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Cities, CitiesAdmin)
admin.site.register(Districts, DistrictsAdmin)
admin.site.register(States, StatesAdmin)
admin.site.register(Countries, CountriesAdmin)
admin.site.register(UserRegistration, UserRegistrationAdmin)
# admin.site.register(Reservation, ReservationAdmin)