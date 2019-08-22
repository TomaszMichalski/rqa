from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from . import models
from datetime import datetime, timedelta
from django.core.exceptions import ValidationError

# form used to gather custom analysis and custom prediction parameters
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

# form used to display and modify analysis and prediction configuration for user and group
class ConfigurationForm(forms.ModelForm):
    class Meta:
        model = models.Configuration
        fields = ('address', 'radius', 'period', 'is_pm1', 'is_pm25', 'is_pm10', 'is_temp', 'is_pressure', 'is_humidity', 'is_wind', 'is_clouds')
        labels = {
            'radius': 'Radius (km)',
            'period': 'Period (days)',
            'is_pm1': 'PM1',
            'is_pm25': 'PM25',
            'is_pm10': 'PM10',
            'is_temp': 'Temperature',
            'is_pressure': 'Pressure',
            'is_humidity': 'Humidity',
            'is_wind': 'Wind',
            'is_clouds': 'Clouds'
        }

# create new group form
class GroupForm(forms.ModelForm):
    class Meta:
        model = models.Group
        fields = ('name', 'key')

    def clean_name(self):
        name = self.cleaned_data['name']
        if models.Group.objects.filter(name=name).exists():
            raise ValidationError("Group with this name already exists")
        return name

    def clean_key(self):
        key = self.cleaned_data['key']
        if models.Group.objects.filter(key=key).exists():
            raise ValidationError("Group with this key already exists")
        return key

# register new user form
class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=32)
    last_name = forms.CharField(max_length=32)
    email = forms.EmailField(max_length=128)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )

