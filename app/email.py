from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def send_email(request, analysis_data):
    subject = 'Generated graph from RQA'
    message = 'Here\'s your generated graph for requested data'
    email_from = 'RQA <' + settings.EMAIL_HOST_USER + '>'
    recipient_list = [request.user.email]
    fail_silently = False
    html_message = render_to_string('app/analysis_chart.html', analysis_data)
    plain_message = strip_tags(html_message)
    send_mail(subject, plain_message, email_from, recipient_list, fail_silently, html_message=html_message)
