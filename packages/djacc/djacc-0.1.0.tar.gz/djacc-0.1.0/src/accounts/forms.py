from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordResetForm
from django.utils.translation import gettext_lazy as _
from .signals import send_activation_email
from threading import Thread
from .defaults import getattribute


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean(self):
        if getattribute('UNIQUE_EMAIL'):
            email = self.cleaned_data.get('email')
            users = User.objects.filter(email__iexact=email)
            if users.exists():
                user = users.last()
                if user.is_active == False:
                    thread = Thread(target=send_activation_email, args=(user,))
                    thread.setDaemon(True)
                    thread.start()
                    msg = _("Email already exists, Activation link has been sent to email!")
                    self.add_error('email', msg)
                else:
                    msg = _("Email already exists!")
                    self.add_error('email', msg)
        return self.cleaned_data


class UserProfile(UserChangeForm):
    password = None
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control mt-1', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control mt-1', 'placeholder': 'Last Name'}),
            'username': forms.TextInput(attrs={'class': 'form-control mt-1', 'placeholder': 'Username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control mt-1', 'placeholder': 'Email'}),
        }


class EmailValidationCheckForm(PasswordResetForm):
    def clean_email(self):
        email = self.cleaned_data['email']
        if not User.objects.filter(email__iexact=email).exists():
            msg = _("There is no user registered with the specified E-Mail address.")
            self.add_error('email', msg)
        return email
