from django.db import models

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

class Installation():
    def __init__(self, id, lat, long):
        self.id = id
        self.lat = lat
        self.lon = lon

    def __str__(self):
        return "[id: %f, lat: %f, lon: %f]" % (self.id, self.lat, self.lon)