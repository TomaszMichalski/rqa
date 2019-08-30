from django.core.mail import send_mail
from django.conf import settings


def send_email(request, recipient):
    subject = 'Thank you for registering to our site'
    message = ' it  means a world to us '
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [recipient]
    send_mail(subject, message, email_from, recipient_list)
