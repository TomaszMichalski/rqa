from django import forms
from . import models
from datetime import datetime

class GenerateForm(forms.Form):
    address = forms.CharField(label='Address')
    radius = forms.CharField(label='Radius (km)')
    date_from = forms.DateTimeField(label='From')
    date_to = forms.DateTimeField(label='To')
    is_pm1 = forms.BooleanField(label='PM1', required=False, initial=True)
    is_pm25 = forms.BooleanField(label='PM2.5', required=False, initial=True)
    is_pm10 = forms.BooleanField(label='PM10', required=False, initial=True)
    is_temp = forms.BooleanField(label='Temperature', required=False, initial=True)
    is_pressure = forms.BooleanField(label='Pressure', required=False, initial=True)
    is_humidity = forms.BooleanField(label='Humidity', required=False, initial=True)
    is_wind = forms.BooleanField(label='Wind', required=False, initial=True)
    is_clouds = forms.BooleanField(label='Clouds', required=False, initial=True)

