from . import models

def create_generation_parameters(form):
    address = form.cleaned_data.get('address')
    date_from = form.cleaned_data.get('date_from')
    date_to = form.cleaned_data.get('date_to')
    is_pm1 = form.cleaned_data.get('is_pm1')
    is_pm25 = form.cleaned_data.get('is_pm25')
    is_pm10 = form.cleaned_data.get('is_pm10')
    return models.GenerationParameters(address, date_from, date_to, is_pm1, is_pm25, is_pm10)