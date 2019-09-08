from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def send_analysis_email(request, analysis_data):
    _send_email(request, analysis_data, 'analysis')


def send_prediction_email(request, prediction_data):
    _send_email(request, prediction_data, 'prediction')


def _send_email(request, data, data_type):
    subject = 'Generated {0} from RQA'.format(data_type)
    email_from = 'RQA <' + settings.EMAIL_HOST_USER + '>'
    recipient_list = [request.user.email]
    fail_silently = False
    template = 'app/{0}_table.html'.format(data_type)
    html_message = render_to_string(template, data)
    plain_message = 'Here\'s your {0} for requested period'.format(data_type) + strip_tags(html_message)
    send_mail(subject, plain_message, email_from, recipient_list, fail_silently, html_message=html_message)
