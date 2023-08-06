from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from .tokens import account_activation_token
from django.conf import settings
from threading import Thread
from .defaults import getattribute


def send_activation_email(user):
    email_subject = "Activate Your Account"
    email_temp = getattribute('ACTIVATION_EMAIL_TEMPLATE')
    template_name = 'accounts/activate.html' if email_temp==True else email_temp
    current_site = getattribute('CURRENT_SITE')
    email_body = render_to_string(template_name, {
        'user': user,
        "domain": "http://127.0.0.1:8000" if current_site==True else current_site,
        "username": urlsafe_base64_encode(force_bytes(user.username)),
        'token': account_activation_token.make_token(user),
    })
    email = EmailMessage(subject=email_subject, body=email_body, from_email=settings.EMAIL_FROM_USER,
    to=[user.email])
    email.send()


@receiver(post_save, sender=User)
def update_user(sender, instance, created, **kwargs):
    if created and getattribute('ACCOUNT_ACTIVATION') and not instance.is_superuser:
            instance.is_active = False
            instance.save()
            thread = Thread(target=send_activation_email, args=(instance,))
            thread.setDaemon(True)
            thread.start()
