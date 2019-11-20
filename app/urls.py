from django.urls import path
from django.contrib.auth import views as auth_views

from app.forms import CustomLoginForm
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('analysis', views.analysis, name='analysis'),
    path('prediction', views.prediction, name='prediction'),
    path('configuration', views.configuration, name='configuration'),
    path('analysis/generate', views.analysis_generate, name='analysis_generate'),
    path('analysis/user', views.analysis_user, name='analysis_user'),
    path('analysis/group', views.analysis_group, name='analysis_group'),
    path('analysis/custom', views.analysis_custom, name='analysis_custom'),
    path('prediction/generate', views.prediction_generate, name='prediction_generate'),
    path('prediction/user', views.prediction_user, name='prediction_user'),
    path('prediction/group', views.prediction_group, name='prediction_group'),
    path('prediction/custom', views.prediction_custom, name='prediction_custom'),
    path('configuration/user', views.configuration_user, name='configuration_user'),
    path('configuration/group', views.configuration_group, name='configuration_group'),
    path('configuration/group/create', views.configuration_group_create, name='configuration_group_create'),
    path('configuration/group/list', views.configuration_group_list, name='configuration_group_list'),
    path('configuration/group/join', views.configuration_group_join, name='configuration_group_join'),
    path('configuration/group/leave', views.configuration_group_leave, name='configuration_group_leave'),
    path('user/register', views.register, name='register'),
    path('user/login', auth_views.LoginView.as_view(authentication_form=CustomLoginForm), name='login'),
    path('user/logout', auth_views.LogoutView.as_view(template_name='registration/logout.html'), name='logout'),
    path('guest/generate', views.guest_generate, name='guest_generate'),
    path('analysis/sendmail', views.send_analysis_email, name='send_analysis_email'),
    path('prediction/sendmail', views.send_prediction_email, name='send_prediction_email'),
    path('analysis/async', views.async_analysis, name='async_analysis'),
    path('prediction/async', views.async_prediction, name='async_prediction'),
]