from django.urls import path
from django.contrib.auth import views as auth_views
from .defaults import getattribute
from .views import (
    SignUp, Login, ActivateUser, Profile,
    PasswordChange, PasswordReset, PasswordResetConfirm
    )

signupattr =  getattribute('SIGNUP_URL')
signup = 'signup/' if signupattr == True else signupattr
signinattr = getattribute('SIGNIN_URL')
signin = 'signin/' if signinattr == True else signinattr

urlpatterns = [
    path(signup, SignUp.as_view(), name='signup'),
    path(signin, Login.as_view(), name='signin'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('profile/', Profile.as_view(), name='profile'),
    path('change-password/', PasswordChange.as_view(), name='change-password'),
    path('forget/', PasswordReset.as_view(), name='reset-password'),
    path('forget/<uidb64>/<token>/', PasswordResetConfirm.as_view(), name='password_reset_confirm'),
]
if getattribute('ACCOUNT_ACTIVATION'): urlpatterns.append(
    path('account-activation/<str:username>/<str:token>/', ActivateUser.as_view(), name='account-activation')
)
