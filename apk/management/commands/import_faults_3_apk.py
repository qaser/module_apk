import csv

from django.core.management import BaseCommand

from apk.models import Act, Control, Department, Fault, Location, Profile


class Command(BaseCommand):
    help = 'Update database'

    def handle(self, *args, **options):
        user = Profile.objects.get(user__username='aa.lomakin')
        with open('csv/faults_3_apk.csv', encoding='utf-8') as file:
            reader = csv.reader(file)
            for i, row in enumerate(reader):
                num, dep, obj, des, doc, group, date = row
                if i:
                    department, _ = Department.objects.get_or_create(title=dep)
                    location, _ = Location.objects.get_or_create(
                        department=department,
                        object=obj,
                    )
                    control_level = Control.objects.get(
                        slug='3_apk'
                    )
                    act, _ = Act.objects.get_or_create(
                        control_level=control_level,
                        act_year='2019',
                        act_number=2,
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
                        intruder=Profile.objects.get(department=department),
                        unseeing=Profile.objects.get(department=department),
                    )
