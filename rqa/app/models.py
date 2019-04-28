from django.db import models

class GenerationParameters():
    def __init__(self, address, radius, date_from, date_to, is_pm1, is_pm25, is_pm10):
        self.address = address
        self.radius = radius
        self.date_from = date_from
        self.date_to = date_to
        self.is_pm1 = is_pm1
        self.is_pm25 = is_pm25
        self.is_pm10 = is_pm10

    def __str__(self):
        return "[address: %s, radius: %s, date_from: %s, date_to: %s, is_pm1: %s, is_pm25: %s, is_pm10: %s]" % (self.address, self.radius, self.date_from, self.date_to, self.is_pm1, self.is_pm25, self.is_pm10)
