from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta

class GenerationParameters():
    def __init__(self, address, radius, date_from, date_to, is_pm1, is_pm25, is_pm10, is_temp, is_pressure, is_humidity, is_wind, is_clouds):
        self.address = address
        self.radius = radius
        self.date_from = date_from
        self.date_to = date_to
        self.is_pm1 = is_pm1
        self.is_pm25 = is_pm25
        self.is_pm10 = is_pm10
        self.is_temp = is_temp
        self.is_pressure = is_pressure
        self.is_humidity = is_humidity
        self.is_wind = is_wind
        self.is_clouds = is_clouds

    def __str__(self):
        return "[address: %s, radius: %s, date_from: %s, date_to: %s, is_pm1: %s, is_pm25: %s, is_pm10: %s, is_temp: %s, is_pressure: %s, is_humidity: %s, is_wind: %s, is_clouds: %s]" % (self.address, self.radius, self.date_from, self.date_to, self.is_pm1, self.is_pm25, self.is_pm10, self.is_temp, self.is_pressure, self.is_humidity, self.is_wind, self.is_clouds)

class Address():
    def __init__(self, id, lat, lon):
        self.id = id
        self.lat = lat
        self.lon = lon

    def __str__(self):
        return "[id: %f, lat: %f, lon: %f]" % (self.id, self.lat, self.lon)

class Configuration(models.Model):
    address = models.CharField(max_length=128)
    radius = models.CharField(max_length=8)
    period = models.CharField(max_length=4)
    is_pm1 = models.BooleanField(default=True)
    is_pm25 = models.BooleanField(default=True)
    is_pm10 = models.BooleanField(default=True)
    is_temp = models.BooleanField(default=True)
    is_pressure = models.BooleanField(default=True)
    is_humidity = models.BooleanField(default=True)
    is_wind = models.BooleanField(default=True)
    is_clouds = models.BooleanField(default=True)

class Group(models.Model):
    name = models.CharField(max_length=64)
    analysis_configuration = models.OneToOneField(Configuration, null=True, on_delete=models.SET_NULL, related_name="group_analysis_configuration")
    prediction_configuration = models.OneToOneField(Configuration, null=True, on_delete=models.SET_NULL, related_name="group_prediction_configuration")

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    analysis_configuration = models.OneToOneField(Configuration, null=True, on_delete=models.SET_NULL, related_name="analysis_configuration")
    prediction_configuration = models.OneToOneField(Configuration, null=True, on_delete=models.SET_NULL, related_name="prediction_configuration")
    group = models.OneToOneField(Group, null=True, on_delete=models.SET_NULL)