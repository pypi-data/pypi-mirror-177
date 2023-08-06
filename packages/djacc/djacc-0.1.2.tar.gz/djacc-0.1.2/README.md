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

```