# djaccounts
Please also add these lines in your settings.py file!


"""

INSTALLED_APPS.append('accounts')
INSTALLED_APPS.append('crispy_forms')

CRISPY_TEMPLATE_PACK = 'bootstrap4'

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'accounts.authentication.EmailOrUsernameModelBackend',
)

"""