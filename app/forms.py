from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from . import consts
from . import db
from . import models
from . import util
from datetime import datetime, timedelta
from django.core.exceptions import ValidationError

# form used to gather custom analysis and custom prediction parameters
class GenerateForm(forms.Form):
    address = forms.CharField(label='Address')
    radius = forms.CharField(label='Radius (km)')
    date_from = forms.DateTimeField(label='From', error_messages={ 'invalid': consts.INVALID_DATE_FROM_MESSAGE })
    date_to = forms.DateTimeField(label='To', error_messages={ 'invalid': consts.INVALID_DATE_TO_MESSAGE })
    is_pm1 = forms.BooleanField(label='PM1', required=False, initial=True)
    is_pm25 = forms.BooleanField(label='PM2.5', required=False, initial=True)
    is_pm10 = forms.BooleanField(label='PM10', required=False, initial=True)
    is_temp = forms.BooleanField(label='Temperature', required=False, initial=True)
    is_pressure = forms.BooleanField(label='Pressure', required=False, initial=True)
    is_humidity = forms.BooleanField(label='Humidity', required=False, initial=True)
    is_wind = forms.BooleanField(label='Wind', required=False, initial=True)
    is_clouds = forms.BooleanField(label='Clouds', required=False, initial=True)

    def clean_address(self):
        address = self.cleaned_data['address']
        if not util.is_correct_address(address):
            raise ValidationError(consts.ADDRESS_NOT_RECOGNISED)

        return address

    def clean_radius(self):
        radius = self.cleaned_data['radius']
        if not util.is_positive_number(radius):
            raise ValidationError(consts.RADIUS_SHOULD_BE_POSITIVE_NUMBER)
        return radius

    def clean(self):
        cleaned_data = super().clean()

        date_from = cleaned_data.get('date_from')
        date_to = cleaned_data.get('date_to')
        if date_from and date_to:
            if date_from >= date_to:
                raise ValidationError(consts.DATE_TO_MUST_BE_GREATER_THAN_DATE_FROM)

        address = cleaned_data.get('address')
        radius = cleaned_data.get('radius')
        if address and radius:
            try:
                lat, lon = util.get_geo_location(address)
            except:
                return False
            if not db.is_location_supported(lat, lon, float(radius)):
                raise ValidationError(consts.ADDRESS_NOT_SUPPORTED)

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

    def clean_radius(self):
        radius = self.cleaned_data['radius']
        if not util.is_positive_number(radius):
            raise ValidationError(consts.RADIUS_SHOULD_BE_POSITIVE_NUMBER)
        return radius

    def clean_period(self):
        period = self.cleaned_data['period']
        if not util.is_positive_number(period):
            raise ValidationError(consts.PERIOD_SHOULD_BE_POSITIVE_NUMBER)
        return period

    def clean(self):
        cleaned_data = super().clean()

        address = cleaned_data.get('address')
        radius = cleaned_data.get('radius')
        if address and radius:
            try:
                lat, lon = util.get_geo_location(address)
                if not db.is_location_supported(lat, lon, float(radius)):
                    raise ValidationError(consts.ADDRESS_NOT_SUPPORTED)
            except:
                raise ValidationError(consts.ADDRESS_NOT_RECOGNISED)

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

