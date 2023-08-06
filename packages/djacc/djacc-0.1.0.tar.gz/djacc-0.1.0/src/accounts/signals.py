from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from .tokens import account_activation_token
from django.conf import settings
from threading import Thread
from .defaults import getattribute

def send_activation_email(user):
    current_site = Site.objects.get_current().domain
    email_subject = "Activate Your Account"
    if getattribute('CUSTOM_EMAIL_TEMPLATE') != True:
        template_name = getattribute('CUSTOM_EMAIL_TEMPLATE')
    else:
        template_name = 'accounts/activate.html'
    email_body = render_to_string(template_name, {
        'user': user,
        "domain": current_site,
        "username": urlsafe_base64_encode(force_bytes(user.username)),
        'token': account_activation_token.make_token(user),
    })
    email = EmailMessage(subject=email_subject, body=email_body, from_email=settings.EMAIL_FROM_USER,
    to=[user.email])
    email.send()
    

@receiver(post_save, sender=User)
def update_user(sender, instance, created, **kwargs):
    if created and getattribute('ACCOUNT_ACTIVATION'):
        instance.is_active = False
        instance.save()
        thread = Thread(target=send_activation_email, args=(instance,))
        thread.setDaemon(True)
        thread.start()
