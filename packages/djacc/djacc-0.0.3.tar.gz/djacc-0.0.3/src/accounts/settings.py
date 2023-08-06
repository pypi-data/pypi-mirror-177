from django.conf import settings

INSTALLED_APPS + ['djaccounts', 'crispy_forms']

CRISPY_TEMPLATE_PACK = 'bootstrap4'

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'accounts.authentication.EmailOrUsernameModelBackend',
)
