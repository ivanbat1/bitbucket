from django import forms
from django.forms import ModelForm
from .models import *


class DateInput(forms.DateInput):
    input_type = 'date'

class AddWorker(forms.Form, ModelForm):
    class Meta():
        model = GeneralR
        exclude = ['']
        widgets = {
            'create_data': DateInput()
        }


class ChangeWorker(forms.Form, ModelForm):
    class Meta:
        model = GeneralR
        exclude = ['parent']


