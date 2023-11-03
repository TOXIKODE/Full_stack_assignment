from django.db import models

# Create your models here.
class Device(models.Model):
    uid = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)

class TemperatureReading(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    start_on = models.DateTimeField(null=True,blank=True)
    end_on = models.DateTimeField(null=True,blank=True)
    temperature = models.FloatField()

class HumidityReading(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    start_on = models.DateTimeField(null=True,blank=True)
    end_on = models.DateTimeField(null=True,blank=True)
    humidity = models.FloatField()
