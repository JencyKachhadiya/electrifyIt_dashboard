from django.db import models

# Create your models here.
class Vehicle(models.Model):
    license_plate = models.CharField(max_length=10)
    make = models.CharField(max_length=50)
    vin = models.CharField(max_length=50)
    model = models.CharField(max_length=100)
    vehicle_type = models.CharField(max_length=50)
    date = models.DateField()
    miles_driven = models.IntegerField()

    def __str__(self):
        return self.license_plate