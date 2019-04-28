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

