"""
Definition of forms.
"""

from .models import *
from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _


class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'User name'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Password'}))


class ReportForm(ModelForm):
    class Meta:
        model = Report
        exclude = ['creator']


class ItemForm(ModelForm):
    class Meta:
        model = Item
        exclude = ['creator', 'report']