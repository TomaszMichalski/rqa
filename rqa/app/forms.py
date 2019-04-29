from django import forms
from . import models
from datetime import datetime

class GenerateForm(forms.Form):
    address = forms.CharField(label='Adres')
    radius = forms.CharField(label='Promień (km)')
    date_from = forms.DateTimeField(label='Od')
    date_to = forms.DateTimeField(label='Do')
    is_pm1 = forms.BooleanField(label='PM1', required=False, initial=True)
    is_pm25 = forms.BooleanField(label='PM2.5', required=False, initial=True)
    is_pm10 = forms.BooleanField(label='PM10', required=False, initial=True)
    is_temp = forms.BooleanField(label='Temperatura', required=False, initial=True)
    is_pressure = forms.BooleanField(label='Ciśnienie', required=False, initial=True)
    is_humidity = forms.BooleanField(label='Wilgotność', required=False, initial=True)
    is_wind = forms.BooleanField(label='Wiatr', required=False, initial=True)
    is_clouds = forms.BooleanField(label='Zachmurzenie', required=False, initial=True)

