from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.utils.translation import ugettext_lazy as _

class AccountAuthenticationForm(AuthenticationForm):
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control'}))

class AccountUserCreationForm(UserCreationForm):
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control'}))
    password1 = forms.CharField(label=_("Password1"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control'}))
    password2 = forms.CharField(label=_("Password2"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control'}))