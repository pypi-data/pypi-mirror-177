from django.views import View
from django.shortcuts import redirect, HttpResponse
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView, PasswordResetView, PasswordResetConfirmView
from django.utils.http import urlsafe_base64_decode
from .tokens import account_activation_token
from django.utils.encoding import force_str
from .forms import (
    UserRegisterForm, UserProfile,
    EmailValidationCheckForm
    )
from django.contrib.auth.models import User
from .signals import send_activation_email
from threading import Thread
from .defaults import getattribute


class SignUp(SuccessMessageMixin, CreateView):
    form_class = UserRegisterForm
    sig_temp = getattribute('SIGNUP_TEMPLATE')
    template_name = sig_temp if sig_temp!=True else "accounts/register.html"
    success_url = reverse_lazy('signin')
    success_message = "Your account created successfully!"
    if getattribute('ACCOUNT_ACTIVATION'):
        success_message = "Please check your mail to verify!"


class ActivateUser(View):
    def get(self, request, username, token):
        try:
            encUser = force_str(urlsafe_base64_decode(username))
            user = User.objects.filter(username=encUser)
            if user.exists():
                user = user.last()
            else: raise 'Email not found!'
        except Exception:
            user = None

        if user != None:
            if account_activation_token.check_token(user, token):
                user.is_active = True
                user.save()
                messages.add_message(request, messages.SUCCESS, 'Your account successfully activated!')
            else:
                thread = Thread(target=send_activation_email, args=(user,))
                thread.setDaemon(True)
                thread.start()
                messages.add_message(request, messages.SUCCESS, 'Link is expired! A new link sent to your mail!')
            return redirect('signin')
        return HttpResponse('Invalid login!')


class Login(SuccessMessageMixin, LoginView):
    sig_temp = getattribute('LOGIN_TEMPLATE')
    template_name = sig_temp if sig_temp!=True else 'accounts/login.html'
    success_url = reverse_lazy('index')
    success_message = "Login successful!"


class Profile(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    form_class = UserProfile
    pro_temp = getattribute('PROFILE_TEMPLATE')
    template_name = pro_temp if pro_temp!=True else 'accounts/profile.html'
    success_url = reverse_lazy('index')
    success_message = "Your profile updated successfully!"
    def get_object(self):
        return self.request.user


class PasswordChange(SuccessMessageMixin, LoginRequiredMixin, PasswordChangeView):
    template_name = 'accounts/change-password.html'
    success_url = reverse_lazy('index')
    success_message = "Your password was changed successfully"


class PasswordReset(SuccessMessageMixin, PasswordResetView):
    for_temp = getattribute('FORGET_TEMPLATE')
    template_name = for_temp if for_temp!=True else 'accounts/reset-password.html'
    success_url = reverse_lazy('signin')
    success_message = "Your password reset request was sent"
    form_class = EmailValidationCheckForm


class PasswordResetConfirm(SuccessMessageMixin, PasswordResetConfirmView):
    template_name = 'accounts/reset-password-confirm.html'
    success_url = reverse_lazy('signin')
    success_message = "Your password reset was done successfully"
