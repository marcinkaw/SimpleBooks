"""
Definition of forms.
"""

from .models import *
from django import forms
from django.forms import ModelForm, DateField
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

    def __init__(self, *args, **kwargs):
        super(ReportForm, self).__init__(*args, **kwargs)
        self.fields['fromDate'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['toDate'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['book'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['currency'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['transferAmount'].widget.attrs.update({
            'class': 'form-control'
        })


class ItemForm(ModelForm):
    class Meta:
        model = Item
        exclude = ['creator', 'report']

    def __init__(self, *args, **kwargs):
        super(ItemForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['itemDirection'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['itemDate'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['party'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['amount'].widget.attrs.update({
            'class': 'form-control'
        })


