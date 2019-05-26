from django.shortcuts import render
from . import forms
from . import models
from . import util
from . import db
import json

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

def analysis_user(request):
    data = dict()
    info = []

    return render(request, 'app/analysis_chart.html', { 'data': data, 'info': info })

def analysis_group(request):
    data = dict()
    info = []

    return render(request, 'app/analysis_chart.html', { 'data': data, 'info': info })

def analysis_custom(request):
    form = forms.GenerateForm(request.GET)
    if form.is_valid():
        generation_parameters = util.create_generation_parameters(form)
        data = db.get_analysis_data(generation_parameters)
        info = data['info']
        data = json.dumps(data)

        return render(request, 'app/analysis_chart.html', { 'data': data, 'info': info })
        
    return render(request, 'app/analysis_generate.html', { 'form': form })

def prediction_generate(request):
    form = forms.GenerateForm()

    return render(request, 'app/prediction_generate.html', { 'form': form })

def prediction_user(request):
    data = dict()
    info = []

    return render(request, 'app/prediction_chart.html', { 'data': data, 'info': info })

def prediction_group(request):
    data = dict()
    info = []

    return render(request, 'app/prediction_chart.html', { 'data': data, 'info': info })

def prediction_custom(request):
    form = forms.GenerateForm(request.GET)
    if form.is_valid():
        generation_parameters = util.create_generation_parameters(form)
        data = dict()
        info = []

        return render(request, 'app/prediction_chart.html', { 'data': data, 'info': info })

    return render(request, 'app/prediction_generate.html', { 'form': form })
