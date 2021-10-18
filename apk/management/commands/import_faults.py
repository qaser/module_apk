import csv

from django.core.management import BaseCommand

from apk.models import Location, Department, Fault, Act, Control, Profile


class Command(BaseCommand):
    help = 'Update database'

    def handle(self, *args, **options):
        user = Profile.objects.get(user__username='huji')
        with open('csv/faults.csv', encoding='utf-8') as file:
            reader = csv.reader(file)
            for i, row in enumerate(reader):
                num, group, dep, obj, des, doc, date = row
                if i:
                    department, _ = Department.objects.get_or_create(title=dep)
                    location, _ = Location.objects.get_or_create(
                        department=department,
                        object=obj,
                    )
                    control_level = Control.objects.get(
                        slug='1_apk'
                    )
                    act, _ = Act.objects.get_or_create(
                        control_level=control_level,
                        act_year='2021',
                        act_number=1,
                        )
                    Fault.objects.get_or_create(
                        fault_number=num,
                        fault_date=date,
                        group=group,
                        act=act,
                        location=location,
                        description=des,
                        document=doc,
                        inspector=user,
                    )
