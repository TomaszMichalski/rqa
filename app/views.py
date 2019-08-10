from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.contrib.auth import login as django_login
from . import forms
from . import models
from . import util
from . import db
from . import consts
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

def home(request):
    if request.user.is_authenticated:
        return render(request, 'app/home.html')
    
    return render(request, 'app/guest.html')

@login_required(login_url='user/login')
def analysis(request):
    return render(request, 'app/analysis.html')

@login_required(login_url='user/login')
def prediction(request):
    return render(request, 'app/prediction.html')

@login_required(login_url='user/login')
def configuration(request):
    profile = models.Profile.objects.get(user=request.user)
    analysis_configuration = profile.analysis_configuration
    prediction_configuration = profile.prediction_configuration
    if request.method == "POST":
        analysis_configuration_form = forms.ConfigurationForm(request.POST, instance=analysis_configuration, prefix='analysis')
        prediction_configuration_form = forms.ConfigurationForm(request.POST, instance=prediction_configuration, prefix='prediction')
        if analysis_configuration_form.is_valid() and prediction_configuration_form.is_valid():
            analysis_configuration_form.save()
            prediction_configuration_form.save()
    else:
        analysis_configuration_form = forms.ConfigurationForm(instance=analysis_configuration, prefix='analysis')
        prediction_configuration_form = forms.ConfigurationForm(instance=prediction_configuration, prefix='prediction')
    
    return render(request, 'app/configuration.html', { 'analysis_configuration': analysis_configuration_form, 'prediction_configuration': prediction_configuration_form })

@login_required(login_url='user/login')
def analysis_generate(request):
    form = forms.GenerateForm()

    return render(request, 'app/analysis_generate.html', { 'form': form })

@login_required(login_url='user/login')
def analysis_user(request):
    profile = models.Profile.objects.get(user=request.user)
    analysis_configuration = profile.analysis_configuration
    generation_parameters = util.convert_to_generation_parameters(analysis_configuration)
    data = db.get_analysis_data(generation_parameters)
    info = data['info']
    data = json.dumps(data)

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
    profile = models.Profile.objects.get(user=request.user)
    prediction_configuration = profile.prediction_configuration
    generation_parameters = util.convert_to_generation_parameters(prediction_configuration, True)
    data = db.get_prediction_data(generation_parameters)
    info = data['info']
    data = json.dumps(data)

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

def guest_generate(request):
    location = request.GET.get('location', None)
    if location is None:
        return redirect('guest')
    
    generation_parameters = util.create_guest_generation_parameters(location)
    data = db.get_prediction_data(generation_parameters)
    info = data['info']
    info.append(consts.GUEST_MESSAGE)
    data = json.dumps(data)
    chart_title = util.get_chart_title(generation_parameters.address, generation_parameters.date_from, generation_parameters.date_to)

    return render(request, 'app/guest_chart.html', { 'data': data, 'info': info, 'chart_title': chart_title })