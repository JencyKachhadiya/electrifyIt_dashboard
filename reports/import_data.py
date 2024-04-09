import csv
from datetime import datetime
from reports.models import *

def import_csv_data(file_path):
    try:
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                Vehicle.objects.create(
                    license_plate=row['license_plate'],
                    make=row['make'],
                    vin=row['vin'],
                    model=row['model'],
                    vehicle_type=row['vehicle_type'],
                    date=datetime.strptime(row['date'], '%Y-%m-%d').date(),
                    miles_driven=int(row['miles_driven'])
                )
    except (FileNotFoundError, ValueError) as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    file_path = 'data.csv'
    import_csv_data(file_path)
