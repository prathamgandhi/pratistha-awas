from django.core.management.base import BaseCommand
from awas.models import Cities, CitiesLocal, Districts, DistrictsLocal, States, StatesLocal, Countries, CountriesLocal

class Command(BaseCommand):
    help = "Run only once, used for populating database tables like cities, districts, states and countries"

    def handle(self, *args, **options):
        all_cities = Cities.objects.using('remote').all()
        for city in all_cities.values():
            CitiesLocal.objects.create(**city)
        all_districts = Districts.objects.using('remote').all()
        for district in all_districts.values():
            DistrictsLocal.objects.create(**district)
        all_states = States.objects.using('remote').all()
        for state in all_states.values():
            StatesLocal.objects.create(**state)
        all_countries = Countries.objects.using('remote').all()
        for country in all_countries.values():
            CountriesLocal.objects.create(**country)
