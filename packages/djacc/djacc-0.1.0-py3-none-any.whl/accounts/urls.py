from django.urls import path
from django.contrib.auth import views as auth_views
from .defaults import getattribute
from .views import (
    SignUp, Login, ActivateUser, Profile,
    PasswordChange, PasswordReset, PasswordResetConfirm
    )

signupattr =  getattribute('SIGNUP_URL')
signup = 'signup/' if signupattr == True else signupattr
signin = 'signin/' if getattribute('SIGNIN_URL') == True else getattribute('SIGNIN_URL')

app_name = 'accounts'
urlpatterns = [
    path(signup, SignUp.as_view(), name='signup'),
    path(signin, Login.as_view(), name='signin'),
    path('account-activation/<str:username>/<str:token>/', ActivateUser.as_view(), name='account-activation'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('profile/', Profile.as_view(), name='profile'),
    path('change-password/', PasswordChange.as_view(), name='change-password'),
    path('reset-password/', PasswordReset.as_view(), name='reset-password'),
    path('reset-password-confirm/<uidb64>/<token>/', PasswordResetConfirm.as_view(), name='password_reset_confirm'),
]
