from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import PasswordResetForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from account.models import UserProfile
from django.utils.translation import gettext_lazy as _
from django.contrib import messages


class UserRegistrationForm(forms.ModelForm):
    email = forms.EmailField()
    password1 = forms.CharField(label='password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)

    class Meta:
        model = UserProfile
        fields = ["email", "password1", "password2"]

    def email_clean(self):
        email = self.cleaned_data['email'].lower()
        new = User.objects.filter(email=email)
        if new.count():
            raise ValidationError(" Email Already Exist")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']

        if password1 and password2 and password1 != password2:
            raise ValidationError("Password and Confirm password does not match!!")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user


class UserLoginForm(AuthenticationForm):

    error_messages = {
        "invalid_login": _("Please enter a correct email address and password or check that you have conformed your mail address"),
        "inactive": _("Please confirm your email address!"),
    }

    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = "Email"
