from django.shortcuts import render
from . import forms
from . import models

def home(request):
    return render(request, 'app/home.html')

def analysis(request):
    return render(request, 'app/analysis.html')

def prediction(request):
    return render(request, 'app/prediction.html')

def configuration(request):
    return render(request, 'app/configuration.html')

def analysis_generate(request):
    form = forms.AnalysisGenerateForm()

    return render(request, 'app/analysis_generate.html', { 'form': form })

def analysis_chart(request):
    form = forms.AnalysisGenerateForm(request.GET)
    if form.is_valid():
        date_from = form.cleaned_data.get('date_from')
        date_to = form.cleaned_data.get('date_to')
        is_pm1 = form.cleaned_data.get('is_pm1')
        is_pm25 = form.cleaned_data.get('is_pm25')
        is_pm10 = form.cleaned_data.get('is_pm10')
        analysis_parameters = models.AnalysisParameters(date_from, date_to, is_pm1, is_pm25, is_pm10)
    return render(request, 'app/analysis_chart.html', { 'data': analysis_parameters })
