from django import forms
from registration.forms import RegistrationForm


class LoginForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(widget=forms.PasswordInput)
    # password = forms.PasswordInput()


class RegisterForm(RegistrationForm):
    username = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=75)
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)
