from django.conf import settings

UNIQUE_EMAIL = False
ACCOUNT_ACTIVATION = False
LOGIN_TEMPLATE = 'path'
SIGNUP_TEMPLATE = 'path/index.html'
ACTIVATION_EMAIL_TEMPLATE = 'path'
FORGET_TEMPLATE = 'path'
SIGNUP_URL = 'register/'
SIGNIN_URL = 'login/'
PROFILE_TEMPLATE = 'path'


def getattribute(attr):
    return getattr(settings, attr, True)
