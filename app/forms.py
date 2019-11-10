from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.forms import TextInput, PasswordInput, EmailInput, DateInput, CheckboxInput, Field

from . import consts
from . import db
from . import models
from . import util
from datetime import datetime, timedelta
from django.core.exceptions import ValidationError

# used to check if field is a checkbox
setattr(Field, 'is_checkbox', lambda self: isinstance(self.widget, forms.CheckboxInput))


# form used to gather custom analysis and custom prediction parameters
class GenerateForm(forms.Form):
    address = forms.CharField(label='Address',
                              widget=TextInput(attrs={'class': 'validate form-control', 'placeholder': 'Address'}))
    radius = forms.CharField(label='Radius (km)',
                             widget=TextInput(attrs={'class': ' form-control validate', 'placeholder': 'Radius (km)'}))

    date_from = forms.DateTimeField(label='From',
                                    error_messages={'invalid': consts.INVALID_DATE_FROM_MESSAGE},
                                    widget=DateInput(
                                        attrs={'class': 'form-control', 'type': 'date', 'placeholder': 'From Date'}))
    date_to = forms.DateTimeField(label='To',
                                  error_messages={'invalid': consts.INVALID_DATE_FROM_MESSAGE},
                                  widget=DateInput(
                                      attrs={'class': 'form-control', 'type': 'date', 'placeholder': 'To Date'}))

    is_pm1 = forms.BooleanField(label='PM1', required=False, initial=True,
                                widget=CheckboxInput(
                                    attrs={'type': 'checkbox', 'class': 'form-check-input', 'id': 'is_pm1'}))
    is_pm25 = forms.BooleanField(label='PM2.5', required=False, initial=True,
                                 widget=CheckboxInput(
                                     attrs={'type': 'checkbox', 'class': 'form-check-input', 'id': 'is_pm25'}))
    is_pm10 = forms.BooleanField(label='PM10', required=False, initial=True,
                                 widget=CheckboxInput(
                                     attrs={'type': 'checkbox', 'class': 'form-check-input', 'id': 'is_pm10'}))
    is_temp = forms.BooleanField(label='Temperature', required=False, initial=True,
                                 widget=CheckboxInput(
                                     attrs={'type': 'checkbox', 'class': 'form-check-input', 'id': 'is_temp'}))
    is_pressure = forms.BooleanField(label='Pressure', required=False, initial=True,
                                     widget=CheckboxInput(
                                         attrs={'type': 'checkbox', 'class': 'form-check-input', 'id': 'is_pressure'}))
    is_humidity = forms.BooleanField(label='Humidity', required=False, initial=True,
                                     widget=CheckboxInput(
                                         attrs={'type': 'checkbox', 'class': 'form-check-input', 'id': 'is_humidity'}))
    is_wind = forms.BooleanField(label='Wind', required=False, initial=True,
                                 widget=CheckboxInput(
                                     attrs={'type': 'checkbox', 'class': 'form-check-input', 'id': 'is_wind'}))
    is_clouds = forms.BooleanField(label='Clouds', required=False, initial=True,
                                   widget=CheckboxInput(
                                       attrs={'type': 'checkbox', 'class': 'form-check-input', 'id': 'is_clouds'}))

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

    address = forms.CharField(label='Address',
                              widget=TextInput(attrs={'class': 'validate form-control', 'placeholder': 'Address'}))
    radius = forms.CharField(label='Radius (km)',
                             widget=TextInput(attrs={'class': ' form-control validate', 'placeholder': 'Radius (km)'}))

    period = forms.CharField(label='Period (days)',
                             widget=TextInput(attrs={'class': ' form-control validate', 'placeholder': 'Period (days)'}))

    is_pm1 = forms.BooleanField(label='PM1', required=False, initial=True,
                                widget=CheckboxInput(
                                    attrs={'type': 'checkbox', 'class': 'form-check-input', 'id': 'is_pm1'}))
    is_pm25 = forms.BooleanField(label='PM2.5', required=False, initial=True,
                                 widget=CheckboxInput(
                                     attrs={'type': 'checkbox', 'class': 'form-check-input', 'id': 'is_pm25'}))
    is_pm10 = forms.BooleanField(label='PM10', required=False, initial=True,
                                 widget=CheckboxInput(
                                     attrs={'type': 'checkbox', 'class': 'form-check-input', 'id': 'is_pm10'}))
    is_temp = forms.BooleanField(label='Temperature', required=False, initial=True,
                                 widget=CheckboxInput(
                                     attrs={'type': 'checkbox', 'class': 'form-check-input', 'id': 'is_temp'}))
    is_pressure = forms.BooleanField(label='Pressure', required=False, initial=True,
                                     widget=CheckboxInput(
                                         attrs={'type': 'checkbox', 'class': 'form-check-input', 'id': 'is_pressure'}))
    is_humidity = forms.BooleanField(label='Humidity', required=False, initial=True,
                                     widget=CheckboxInput(
                                         attrs={'type': 'checkbox', 'class': 'form-check-input', 'id': 'is_humidity'}))
    is_wind = forms.BooleanField(label='Wind', required=False, initial=True,
                                 widget=CheckboxInput(
                                     attrs={'type': 'checkbox', 'class': 'form-check-input', 'id': 'is_wind'}))
    is_clouds = forms.BooleanField(label='Clouds', required=False, initial=True,
                                   widget=CheckboxInput(
                                       attrs={'type': 'checkbox', 'class': 'form-check-input', 'id': 'is_clouds'}))

    class Meta:
        model = models.Configuration
        fields = (
            'address', 'radius', 'period', 'is_pm1', 'is_pm25', 'is_pm10', 'is_temp', 'is_pressure', 'is_humidity',
            'is_wind', 'is_clouds')
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
    name = forms.CharField(widget=TextInput(attrs={'class': 'validate', 'placeholder': 'Name'}))
    key = forms.CharField(widget=TextInput(attrs={'class': 'validate', 'placeholder': 'Key'}))

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
    username = forms.CharField(widget=TextInput(attrs={'class': 'validate form-control ', 'placeholder': 'Username'}))
    first_name = forms.CharField(
        widget=TextInput(attrs={'class': 'validate form-control', 'placeholder': 'First Name'}))
    last_name = forms.CharField(widget=TextInput(attrs={'class': 'validate form-control', 'placeholder': 'Last Name'}))
    email = forms.CharField(widget=EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    password1 = forms.CharField(widget=PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
    password2 = forms.CharField(
        widget=PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2',)


# sign in user form
class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput(attrs={'class': 'validate form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
