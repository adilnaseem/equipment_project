from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db import connection
import csv
from ...models import Airport, EqptType, EqptStatus,PlaceInstallaion
airport_ = 1 # for which airport you are entering data
airport_data = [
    {'name': 'AIIAP Lahore', 'description': '', 'created_by': 1},
    {'name': 'JIAP Karachi', 'description': '', 'created_by': 1}]
eqpt_types = [{'title':'Hand Baggage X-ray Machine','features':''},{'title':'Hold Baggage X-ray Machine','features':''}]
eqpt_status = [{'title':'Installed & SA'},{'title':'Installed & Faulty'},{'title':'Reserve & SA'},{'title':'Reserve & Faulty'},{'title':'Under Condemnation'}]

# Below code to update id column sequence. it was out of seq like 1,3,4,
# with connection.cursor() as cursor:
#             cursor.execute("UPDATE home_airport SET id = nextval('airport_id_seq');")
class Command(BaseCommand):
    help = 'Imports data from a CSV file'
    def handle(self, *args, **options):
        ##-----------------Airports---------------------------
        for row in airport_data:
            try:
                user = User.objects.get(pk=row['created_by'])
                Airport.objects.create(
                    name=row['name'],
                    description=row['description'],
                    created_by=user,
                )
                self.stdout.write(self.style.SUCCESS(f"Airport '{row['name']}' imported successfully."))
            except User.DoesNotExist:
                self.stdout.write(self.style.ERROR(f"User with id {row['created_by']} does not exist."))
        ##------------------Equipment Types------------------------
        for row in eqpt_types:
            try:
                
                EqptType.objects.create(
                    title=row['title'],
                    features=row['features'],
                )
                self.stdout.write(self.style.SUCCESS(f"Eqpttype imported successfully."))
            except User.DoesNotExist:
                self.stdout.write(self.style.ERROR(f"User with id does not exist."))
        ###------------------Equipment Status------------------------
        for row in eqpt_status:
            try:
               
                EqptStatus.objects.create(
                    title=row['title'],
                )
                self.stdout.write(self.style.SUCCESS(f"EqptStatus  imported successfully."))
            except User.DoesNotExist:
                self.stdout.write(self.style.ERROR(f"User with id  does not exist."))
        #---------------Place of Installation-------------
        with open('data_import/Duty Points.csv', 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header row

            for row in reader:
                PlaceInstallaion.objects.create(
                airport = Airport.objects.get(pk=airport_),
                sector = row[3],
                duty_point = row[4],
                call_sign = row[2],
                ### equipment_issued = , ManytoMany Filed Skipped
                description=''
                )
                self.stdout.write(self.style.SUCCESS(f"Duty Point {row[4]} imported successfully."))
        # pass