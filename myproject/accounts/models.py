from django.db import models
from django.contrib.auth.models import User

class Vehicle(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Associate vehicle with a user
    vehicleType = models.CharField(max_length=50)
    vehicleModel = models.CharField(max_length=100)
    modelYear = models.IntegerField()
    rcNumber = models.CharField(max_length=50)
    licenseNumber = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.vehicleType} - {self.vehicleModel} ({self.modelYear})"
