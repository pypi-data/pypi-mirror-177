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


UNIQUE_EMAIL = False # True
ACCOUNT_ACTIVATION = False # True
SIGNUP_URL = 'register/' # 'signup'
SIGNIN_URL = 'login/' # 'signin'

SIGNUP_TEMPLATE = 'your-temp-path/temp-name.html' # 'accounts/register.html'
ACTIVATION_EMAIL_TEMPLATE = 'your-temp-path/temp-name.html' # 'accounts/activate.html'
LOGIN_TEMPLATE = 'your-temp-path/temp-name.html' # 'accounts/login.html'
FORGET_TEMPLATE = 'your-temp-path/temp-name.html' # 'accounts/reset-password.html'
PROFILE_TEMPLATE = 'your-temp-path/temp-name.html' # 'accounts/profile.html'

CURRENT_SITE = 'example.com' # 'localhost:8000'


def getattribute(attr):
    return getattr(settings, attr, True)
