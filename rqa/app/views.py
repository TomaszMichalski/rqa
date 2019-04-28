from django.shortcuts import render
from . import forms
from . import models
from . import util

def home(request):
    return render(request, 'app/home.html')

def analysis(request):
    return render(request, 'app/analysis.html')

def prediction(request):
    return render(request, 'app/prediction.html')

def configuration(request):
    return render(request, 'app/configuration.html')

def analysis_generate(request):
    form = forms.GenerateForm()

    return render(request, 'app/analysis_generate.html', { 'form': form })

def analysis_chart(request):
    form = forms.GenerateForm(request.GET)
    if form.is_valid():
        generation_parameters = util.create_generation_parameters(form)
        
    return render(request, 'app/analysis_chart.html', { 'data': generation_parameters })

def prediction_generate(request):
    form = forms.GenerateForm()

    return render(request, 'app/prediction_generate.html', { 'form': form })

def prediction_chart(request):
    form = forms.GenerateForm(request.GET)
    if form.is_valid():
        generation_parameters = util.create_generation_parameters(form)

    return render(request, 'app/prediction_chart.html', { 'data': generation_parameters })
