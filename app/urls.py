from django.urls import path
from django.contrib.auth import views as auth_views
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
    path('user/register', views.register, name='register'),
    path('user/login', auth_views.LoginView.as_view(template_name='user/login.html'), name='login'),
    path('user/logout', auth_views.LogoutView.as_view(template_name='user/logout.html'), name='logout'),
    path('guest/generate', views.guest_generate, name='guest_generate'),
]