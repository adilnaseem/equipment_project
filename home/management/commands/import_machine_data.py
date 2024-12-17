#to import data from csv file using below code run comand in terminal-> python manage.py import_machine_data
from django.core.management.base import BaseCommand, CommandError
from ...models import Equipment,Airport,PlaceInstallaion,EqptStatus,EqptType
import csv
from datetime import datetime
from django.contrib.auth.models import User
airport_ = 1
class Command(BaseCommand):
    help = 'Imports equipment data from a CSV file'
    
  
    def handle(self, *args, **options):
        file_path = 'data_import/xray machines.csv'

        with open(file_path, 'r',encoding='utf-8') as file:
            reader = csv.reader(file)
            # Assuming the first row contains headers
            headers = next(reader)
            user = User.objects.get(pk=1)
            for row in reader:
                data = dict(zip(headers, row))
                print(data)
                # Create an Equipment instance, handling foreign keys and data cleaning
                stp_status_choices = {
                'p': Equipment.stp['p'],
                'f': Equipment.stp['f'],
            }
                date_obj = datetime.strptime(data['date_of_manufacturing'], '%d-%m-%Y')
                date_of_manufacturing = date_obj.strftime('%Y-%m-%d')
                equipment = Equipment(
                    airport=Airport.objects.get(pk=airport_),  # Assuming 'airport' is a foreign key field
                    manufacturer=data['manufacturer'],
                    made_in=data['made_in'],
                    serial_no=data['serial_no'],
                    type=EqptType.objects.get(pk=data['type']),  # Assuming 'type' is a foreign key field
                    title=data['title'],
                    model=data['model'],
                    status=EqptStatus.objects.get(pk=data['status']),  # Assuming 'status' is a foreign key field
                    stp_status=stp_status_choices.get(data['stp_status']),#data['stp_status'],
                    date_of_manufacturing=date_of_manufacturing,
                    
                    place_of_installation=PlaceInstallaion.objects.get(pk=data['place_of_installation']),  # Assuming 'place_of_installation' is a foreign key field
                    remarks=data['remarks'],
                    description=data['description'],
                    created_by=user,
                    # Handle created_by and created_at if needed
                )

                try:
                    equipment.save()
                    self.stdout.write(self.style.SUCCESS(f"Imported equipment: {equipment}"))
                except Exception as e:
                    self.stderr.write(self.style.ERROR(f"Error importing equipment: {e}"))


# for row in reader:
#                 # Assuming your model fields match the CSV headers and you have appropriate foreign key relationships
#                 Equipment.objects.create(
#                     airport=Airport.objects.get(pk=row[0]),  # Assuming airport ID is in the first column
#                     manufacturer=row[1],
#                     made_in=row[2],
#                     serial_no=row[3],
#                     type=EqptType.objects.get(pk=row[4]),  # Assuming type ID is in the fifth column
#                     title=row[5],
#                     model=row[6],
#                     status=EqptStatus.objects.get(pk=row[7]),  # Assuming status ID is in the eighth column
#                     received_from=row[8],
#                     date_of_installation=row[9],
#                     place_of_installation=PlaceInstallaion.objects.get(pk=row[10]),  # Assuming place of installation ID is in the eleventh column
#                     description=row[11],
#                     created_by=User.objects.get(pk=1),  # Replace 1 with the actual user ID
#                 )