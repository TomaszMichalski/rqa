from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('analysis/', views.analysis, name='analysis'),
    path('prediction/', views.prediction, name='prediction'),
    path('configuration/', views.configuration, name='configuration'),
    path('analysis/generate', views.analysis_generate, name='analysis_generate'),
    path('analysis/chart', views.analysis_chart, name='analysis_chart'),
    path('prediction/generate', views.prediction_generate, name='prediction_generate'),
    path('prediction/chart', views.prediction_chart, name='prediction_chart'),
]