from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.contrib.auth import login as django_login
from . import forms
from . import models
from . import util
from . import db
import json

def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = forms.RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            analysis_configuration = models.Configuration()
            prediction_configuration = models.Configuration()
            analysis_configuration.save()
            prediction_configuration.save()
            profile = models.Profile(user=user, analysis_configuration=analysis_configuration, prediction_configuration=prediction_configuration)
            profile.save()
            django_login(request, user)
            return redirect('home')
    else:
        form = forms.RegisterForm()
    return render(request, 'user/register.html', { 'form': form })

def login(request):
    if request.user.is_authenticated:
        return redirect('home')

    return render(request, 'app/login.html')

@login_required(login_url='user/login')
def logout(request):
    return render(request, 'app/logout.html')

@login_required(login_url='user/login')
def home(request):
    return render(request, 'app/home.html')

@login_required(login_url='user/login')
def analysis(request):
    return render(request, 'app/analysis.html')

@login_required(login_url='user/login')
def prediction(request):
    return render(request, 'app/prediction.html')

@login_required(login_url='user/login')
def configuration(request):
    return render(request, 'app/configuration.html')

@login_required(login_url='user/login')
def analysis_generate(request):
    form = forms.GenerateForm()

    return render(request, 'app/analysis_generate.html', { 'form': form })

@login_required(login_url='user/login')
def analysis_user(request):
    data = dict()
    info = []

    return render(request, 'app/analysis_chart.html', { 'data': data, 'info': info })

@login_required(login_url='user/login')
def analysis_group(request):
    data = dict()
    info = []

    return render(request, 'app/analysis_chart.html', { 'data': data, 'info': info })

@login_required(login_url='user/login')
def analysis_custom(request):
    form = forms.GenerateForm(request.GET)
    if form.is_valid():
        generation_parameters = util.create_generation_parameters(form)
        data = db.get_analysis_data(generation_parameters)
        info = data['info']
        data = json.dumps(data)

        return render(request, 'app/analysis_chart.html', { 'data': data, 'info': info })
        
    return render(request, 'app/analysis_generate.html', { 'form': form })

@login_required(login_url='user/login')
def prediction_generate(request):
    form = forms.GenerateForm()

    return render(request, 'app/prediction_generate.html', { 'form': form })

@login_required(login_url='user/login')
def prediction_user(request):
    data = dict()
    info = []

    return render(request, 'app/prediction_chart.html', { 'data': data, 'info': info })

@login_required(login_url='user/login')
def prediction_group(request):
    data = dict()
    info = []

    return render(request, 'app/prediction_chart.html', { 'data': data, 'info': info })

@login_required(login_url='user/login')
def prediction_custom(request):
    form = forms.GenerateForm(request.GET)
    if form.is_valid():
        generation_parameters = util.create_generation_parameters(form)
        data = db.get_prediction_data(generation_parameters)
        info = data['info']
        data = json.dumps(data)

        return render(request, 'app/prediction_chart.html', { 'data': data, 'info': info })

    return render(request, 'app/prediction_generate.html', { 'form': form })
