# Django Accounts


### Add these lines in your settings.py file!

```

INSTALLED_APPS.append('accounts')

INSTALLED_APPS.append('crispy_forms')

CRISPY_TEMPLATE_PACK = 'bootstrap4'

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'accounts.authentication.EmailOrUsernameModelBackend',
)

```


### Add these lines in your urls.py file!
```

urlpatterns.append(path('accounts/', include('accounts.urls')))

```