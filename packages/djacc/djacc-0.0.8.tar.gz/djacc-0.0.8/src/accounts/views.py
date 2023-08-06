from .forms import *
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView, PasswordResetView, PasswordResetConfirmView


# Create your views here.
class Login(SuccessMessageMixin, LoginView):
    template_name = 'accounts/login.html'
    success_url = reverse_lazy('accounts:index')
    success_message = "Login successful"


class Register(SuccessMessageMixin, CreateView):
    form_class = UserRegisterForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('accounts:signin')
    success_message = "Your profile was created successfully"


class Profile(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    # form_class = UserChangeForm
    form_class = UserProfile
    template_name = 'accounts/profile.html'
    success_url = reverse_lazy('accounts:index')
    success_message = "Your profile updated successfully"
    def get_object(self):
        return self.request.user


class PasswordChange(SuccessMessageMixin, LoginRequiredMixin, PasswordChangeView):
    template_name = 'accounts/change-password.html'
    success_url = reverse_lazy('accounts:index')
    success_message = "Your password was changed successfully"


class PasswordReset(SuccessMessageMixin, PasswordResetView):
    template_name = 'accounts/reset-password.html'
    success_url = reverse_lazy('accounts:signin')
    success_message = "Your password reset request was sent"
    form_class = EmailValidationCheckForm


class PasswordResetConfirm(SuccessMessageMixin, PasswordResetConfirmView):
    template_name = 'accounts/reset-password-confirm.html'
    success_url = reverse_lazy('accounts:signin')
    success_message = "Your password reset was done successfully"
