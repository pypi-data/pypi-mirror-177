from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordResetForm
from django.utils.translation import gettext_lazy as _


class UserRegisterForm(UserCreationForm):
  email = forms.EmailField()
  class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


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
        if not User.objects.filter(email__iexact=email, is_active=True).exists():
            msg = _("There is no user registered with the specified E-Mail address.")
            self.add_error('email', msg)
        return email
