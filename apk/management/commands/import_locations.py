import csv

from django.core.management import BaseCommand

from apk.models import Location, Department


class Command(BaseCommand):
    help = 'Update database'

    def handle(self, *args, **options):
        with open('csv/locations.csv', encoding='utf-8') as file:
            reader = csv.reader(file)
            for i, row in enumerate(reader):
                department, object = row
                if i:
                    department, _ = Department.objects.get_or_create(title=department)
                    Location.objects.get_or_create(
                        department=department,
                        object=object,
                    )
