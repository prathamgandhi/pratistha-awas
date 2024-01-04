from pratishtha_awas.celery import app
from celery import shared_task

from .models import UserRegistration, Guest, CitiesLocal, StatesLocal, CountriesLocal
import json

@shared_task
def sync_guests_with_registration():
    user_registrations = UserRegistration.objects.using('remote').all()
    for user_registration in user_registrations:
        try:
            city_name = CitiesLocal.objects.get(id=user_registration.city_id)
        except CitiesLocal.DoesNotExist:
            city_name = user_registration.city_name
        try:
            state_name = StatesLocal.objects.get(id=user_registration.state_id)
        except StatesLocal.DoesNotExist:
            state_name = user_registration.state_name
        try:
            country_name = CountriesLocal.objects.get(id=user_registration.country_id)
        except CountriesLocal.DoesNotExist:
            country_name = ""

        person_count = len(json.loads(user_registration.members_info))
        guest, created = Guest.objects.get_or_create(
            guest_name=" ".join(filter(None, [
                user_registration.first_name,
                user_registration.middle_name,
                user_registration.last_name])),
            city=city_name,
            mobile_no=user_registration.mobile,
            remark=user_registration.remarks,
            no_of_persons=person_count,
            arrival_date=user_registration.arrival_date,
            departure_date=user_registration.departure_date,
            email=user_registration.email,
            ext_reg_no=user_registration.id,
            # language=,
            state=state_name,
            country=country_name,
            mandal=user_registration.mandal,
        )
    