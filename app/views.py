from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.contrib.auth import login as django_login
from django.core.paginator import Paginator
from . import email
from . import forms
from . import models
from . import util
from . import db
from . import consts
from . import statistics
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
    return render(request, 'app/configuration.html')

@login_required(login_url='user/login')
def configuration_user(request):
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
    
    return render(request, 'app/configuration_user.html', { 'analysis_configuration': analysis_configuration_form, 'prediction_configuration': prediction_configuration_form })

def configuration_group(request):
    profile = models.Profile.objects.get(user=request.user)
    group = profile.group

    if group is None:
        return render(request, 'app/configuration_group_no_config.html')
    else:
        analysis_configuration = group.analysis_configuration
        prediction_configuration = group.prediction_configuration
        if request.method == "POST":
            analysis_configuration_form = forms.ConfigurationForm(request.POST, instance=analysis_configuration, prefix='analysis')
            prediction_configuration_form = forms.ConfigurationForm(request.POST, instance=prediction_configuration, prefix='prediction')
            if analysis_configuration_form.is_valid() and prediction_configuration_form.is_valid():
                updated_analysis_configuration = analysis_configuration_form.save()
                updated_prediction_configuration = prediction_configuration_form.save()
                group.analysis_configuration = updated_analysis_configuration
                group.prediction_configuration = updated_prediction_configuration
                group.save()
        else:
            analysis_configuration_form = forms.ConfigurationForm(instance=analysis_configuration, prefix='analysis')
            prediction_configuration_form = forms.ConfigurationForm(instance=prediction_configuration, prefix='prediction')
        
        return render(request, 'app/configuration_group.html', { 'analysis_configuration': analysis_configuration_form, 'prediction_configuration': prediction_configuration_form, 'group_name': group.name })

@login_required(login_url='user/login')
def configuration_group_create(request):
    profile = models.Profile.objects.get(user=request.user)
    group = profile.group

    if group is not None:
        return render(request, 'app/configuration_group_already_in.html', { 'group_name': group.name })
    else:
        if request.method == "POST":
            form = forms.GroupForm(request.POST)
            if form.is_valid():
                form.save()
                created_group_key = form.cleaned_data.get('key')
                created_group = models.Group.objects.get(key=created_group_key)
                profile.group = created_group
                profile.save()
                return redirect('configuration_group')
        else:
            form = forms.GroupForm()
        return render(request, 'app/configuration_group_create.html', { 'form': form })

@login_required(login_url='user/login')
def configuration_group_list(request):
    profile = models.Profile.objects.get(user=request.user)
    group = profile.group

    if group is not None:
        return render(request, 'app/configuration_group_already_in.html', { 'group_name': group.name })
    else:
        group_list = models.Group.objects.all()
        paginator = Paginator(group_list, 20)
        page = request.GET.get('page')
        groups = paginator.get_page(page)

        return render(request, 'app/configuration_group_list.html', { 'groups': groups })

@login_required(login_url='user/login')
def configuration_group_join(request):
    profile = models.Profile.objects.get(user=request.user)
    group = profile.group

    if group is not None:
        return render(request, 'app/configuration_group_already_in.html', { 'group_name': group.name })
    else:
        if request.method == "POST":
            group_name = request.POST.get('group_name', '')
            group_key = request.POST.get('group_key', '')
            targeted_group = models.Group.objects.get(name=group_name)
            if targeted_group.key == group_key:
                profile.group = targeted_group
                profile.save()
                return redirect('configuration_group')
        else:
            group_name = request.GET.get('group_name', '')
        return render(request, 'app/configuration_group_join.html', { 'group_name': group_name })

@login_required(login_url='user/login')
def configuration_group_leave(request):
    profile = models.Profile.objects.get(user=request.user)
    group = profile.group

    if group is not None:
        profile.group = None
        profile.save()

    return redirect('configuration_group')

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
    info = statistics.append_statistics_info(info, data)
    stats = statistics.get_statistics_for_data(data)
    data = json.dumps(data)
    chart_title = util.get_chart_title(generation_parameters.address, generation_parameters.date_from, generation_parameters.date_to)
    examination_filename = util.get_examination_filename(generation_parameters.address, generation_parameters.date_from, generation_parameters.date_to)

    return render(request, 'app/analysis_chart.html', { 'data': data, 'info': info, 'chart_title': chart_title, 'filename': examination_filename, 'statistics': stats })

@login_required(login_url='user/login')
def analysis_group(request):
    data = dict()
    info = []
    profile = models.Profile.objects.get(user=request.user)
    group = profile.group
    
    if group is None:
        return render(request, 'app/analysis_group_no_config.html')
    else:
        analysis_configuration = group.analysis_configuration
        generation_parameters = util.convert_to_generation_parameters(analysis_configuration)
        data = db.get_analysis_data(generation_parameters)
        info = data['info']
        info = statistics.append_statistics_info(info, data)
        stats = statistics.get_statistics_for_data(data)
        data = json.dumps(data)
        chart_title = util.get_chart_title(generation_parameters.address, generation_parameters.date_from, generation_parameters.date_to)
        examination_filename = util.get_examination_filename(generation_parameters.address, generation_parameters.date_from, generation_parameters.date_to)

        return render(request, 'app/analysis_chart.html', { 'data': data, 'info': info, 'chart_title': chart_title, 'filename': examination_filename, 'statistics': stats })

@login_required(login_url='user/login')
def analysis_custom(request):
    form = forms.GenerateForm(request.GET)
    if form.is_valid():
        generation_parameters = util.create_generation_parameters(form)
        data = db.get_analysis_data(generation_parameters)
        info = data['info']
        info = statistics.append_statistics_info(info, data)
        stats = statistics.get_statistics_for_data(data)
        data = json.dumps(data)
        chart_title = util.get_chart_title(generation_parameters.address, generation_parameters.date_from, generation_parameters.date_to)
        examination_filename = util.get_examination_filename(generation_parameters.address, generation_parameters.date_from, generation_parameters.date_to)

        context = {'data': data, 'info': info, 'chart_title': chart_title, 'filename': examination_filename, 'statistics': stats}

        request.session['analysis_data'] = context

        return render(request, 'app/analysis_chart.html', context)
        
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
    info = statistics.append_statistics_info(info, data)
    stats = statistics.get_statistics_for_data(data)
    data = json.dumps(data)
    chart_title = util.get_chart_title(generation_parameters.address, generation_parameters.date_from, generation_parameters.date_to)
    examination_filename = util.get_examination_filename(generation_parameters.address, generation_parameters.date_from, generation_parameters.date_to)

    return render(request, 'app/prediction_chart.html', { 'data': data, 'info': info, 'chart_title': chart_title, 'filename': examination_filename, 'statistics': stats })

@login_required(login_url='user/login')
def prediction_group(request):
    data = dict()
    info = []
    profile = models.Profile.objects.get(user=request.user)
    group = profile.group

    if group is None:
        return render(request, 'app/prediction_group_no_config.html')
    else:
        prediction_configuration = group.prediction_configuration
        generation_parameters = util.convert_to_generation_parameters(prediction_configuration, True)
        data = db.get_prediction_data(generation_parameters)
        info = data['info']
        info = statistics.append_statistics_info(info, data)
        stats = statistics.get_statistics_for_data(data)
        data = json.dumps(data)
        chart_title = util.get_chart_title(generation_parameters.address, generation_parameters.date_from, generation_parameters.date_to)
        examination_filename = util.get_examination_filename(generation_parameters.address, generation_parameters.date_from, generation_parameters.date_to)

        return render(request, 'app/prediction_chart.html', { 'data': data, 'info': info, 'chart_title': chart_title, 'filename': examination_filename, 'statistics': stats })

@login_required(login_url='user/login')
def prediction_custom(request):
    form = forms.GenerateForm(request.GET)
    if form.is_valid():
        generation_parameters = util.create_generation_parameters(form)
        data = db.get_prediction_data(generation_parameters)
        info = data['info']
        info = statistics.append_statistics_info(info, data)
        stats = statistics.get_statistics_for_data(data)
        data = json.dumps(data)
        chart_title = util.get_chart_title(generation_parameters.address, generation_parameters.date_from, generation_parameters.date_to)
        examination_filename = util.get_examination_filename(generation_parameters.address, generation_parameters.date_from, generation_parameters.date_to)

        return render(request, 'app/prediction_chart.html', { 'data': data, 'info': info, 'chart_title': chart_title, 'filename': examination_filename, 'statistics': stats })

    return render(request, 'app/prediction_generate.html', { 'form': form })

def guest_generate(request):
    location = request.GET.get('location', None)
    if location is None:
        return redirect('guest')
    
    generation_parameters = util.create_guest_generation_parameters(location)
    data = db.get_prediction_data(generation_parameters)
    info = data['info']
    info.append(consts.GUEST_MESSAGE)
    info = statistics.append_statistics_info(info, data)
    stats = statistics.get_statistics_for_data(data)
    data = json.dumps(data)
    chart_title = util.get_chart_title(generation_parameters.address, generation_parameters.date_from, generation_parameters.date_to)
    examination_filename = util.get_examination_filename(generation_parameters.address, generation_parameters.date_from, generation_parameters.date_to)

    return render(request, 'app/guest_chart.html', { 'data': data, 'info': info, 'chart_title': chart_title, 'filename': examination_filename, 'statistics': stats })


@login_required(login_url='user/login')
def send_email(request):
    analysis_data = request.session.get('analysis_data', None)
    email.send_email(request, analysis_data)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
