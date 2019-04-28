from django.db import models

class AnalysisParameters():
    def __init__(self, date_from, date_to, is_pm1, is_pm25, is_pm10):
        self.date_from = date_from
        self.date_to = date_to
        self.is_pm1 = is_pm1
        self.is_pm25 = is_pm25
        self.is_pm10 = is_pm10

    def __str__(self):
        return "[date_from: %s, date_to: %s, is_pm1: %s, is_pm25: %s, is_pm10: %s]" % (self.date_from, self.date_to, self.is_pm1, self.is_pm25, self.is_pm10)