# Django Accounts


### Add these lines in your INSTALLED_APPS of settings.py file!
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


### Add this line in urlpatterns of your root/core urls.py file!
```

path('accounts/', include('accounts.urls')),

```