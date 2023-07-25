from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm


class LoginForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput,
        label="Password",
        required=True,
    )

    class Meta:
        model = User
        fields = ["email", "password"]


class UserRegisterForm(UserCreationForm):
    password1 = forms.CharField(
        widget=forms.PasswordInput,
        label="Password1",
        required=True,
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput,
        label="Password2",
        required=True,
    )

    class Meta:
        model = User
        fields = [
            "email",
            "username",
            "first_name",
            "last_name",
            "gender",
            "profile",
            "password1",
            "password2",
        ]
