# Django Accounts


## Add these lines in your INSTALLED_APPS of settings.py file!
```

# Third party apps!
'accounts',
'crispy_forms',

```


## Add these lines in your settings.py file!
```

CRISPY_TEMPLATE_PACK = 'bootstrap4'

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'accounts.authentication.EmailOrUsernameModelBackend',
)

```


## Add this line in urlpatterns of your root/core urls.py file!
```

path('accounts/', include('accounts.urls')),

```

## Default parameters which you can change in your settings.py
```

UNIQUE_EMAIL = bool # True
ACCOUNT_ACTIVATION = bool # True
SIGNUP_URL = str['uri'] # 'signup/'
SIGNIN_URL = str['uri'] # 'signin/'

SIGNUP_TEMPLATE = str['path'] # 'accounts/register.html'
ACTIVATION_EMAIL_TEMPLATE = str['path'] # 'accounts/activate.html'
LOGIN_TEMPLATE = str['path'] # 'accounts/login.html'
FORGET_TEMPLATE = str['path'] # 'accounts/reset-password.html'
PROFILE_TEMPLATE = str['path'] # 'accounts/profile.html'

CURRENT_SITE = str['url'] # 'http://127.0.0.1:8000'

```