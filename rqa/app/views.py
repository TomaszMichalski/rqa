from django.shortcuts import render

def home(request):
    return render(request, 'app/home.html')

def analysis(request):
    return render(request, 'app/analysis.html')

def prediction(request):
    return render(request, 'app/prediction.html')

def configuration(request):
    return render(request, 'app/configuration.html')
